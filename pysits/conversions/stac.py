#
# Copyright (C) 2025 sits developers.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#

"""STAC conversions."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse

import pystac
from affine import Affine
from numpy import datetime64
from odc.geo.geobox import GeoBox
from odc.geo.geom import CRS
from pandas import DataFrame as PandasDataFrame
from rasterio.warp import transform_bounds

#
# Prefix used by GDAL to read files through HTTP
#
VSICURL_PREFIX = "/vsicurl/"

#
# Host used by Microsoft Planetary Computer to store data
#
MPC_HOST_SUFFIX = "blob.core.windows.net"


#
# Grid operations
#
def files_geobox(files: PandasDataFrame) -> GeoBox:
    """Create the geobox covering all files of a grid group.

    The geobox uses the native resolution and CRS of the files, so data is read
    without resampling.

    Args:
        files (PandasDataFrame): Files of a single grid group.

    Returns:
        GeoBox: Geobox covering all files.
    """
    xres = float(files["xres"].iloc[0])
    yres = float(files["yres"].iloc[0])

    # Extent covering all files of the group
    xmin = float(files["xmin"].min())
    xmax = float(files["xmax"].max())
    ymin = float(files["ymin"].min())
    ymax = float(files["ymax"].max())

    # Shape (rounded, as files of a group share the same grid)
    width = int(round((xmax - xmin) / xres))
    height = int(round((ymax - ymin) / yres))

    return GeoBox(
        shape=(height, width),
        affine=Affine(xres, 0.0, xmin, 0.0, -yres, ymax),
        crs=CRS(str(files["crs"].iloc[0])),
    )


def grid_group_name(files: PandasDataFrame, index: int) -> str:
    """Create a name for a grid group.

    Args:
        files (PandasDataFrame): Files of a single grid group.

        index (int): Position of the group, used when the CRS has no EPSG code.

    Returns:
        str: Group name (e.g., ``epsg32720-10m``).
    """
    crs = CRS(str(files["crs"].iloc[0]))
    resolution = float(files["xres"].iloc[0])

    try:
        crs_name = f"epsg{crs.epsg}" if crs.epsg else f"grid{index}"

    except Exception:
        crs_name = f"grid{index}"

    return f"{crs_name}-{resolution:g}m"


#
# STAC items
#
def stac_items_from_files(files: PandasDataFrame) -> list[pystac.Item]:
    """Create STAC Items from cube files.

    One item is created for each ``(tile, date)``, with one asset per band. All
    item properties come from the cube metadata: no file is read.

    Cubes can have more than one file for the same tile, date and band, as
    collections may have multiple versions of an acquisition. Each version is
    described as its own item, so all of them are used when data is read.

    Args:
        files (PandasDataFrame): Files of a single grid group.

    Returns:
        list[pystac.Item]: Items describing the files.
    """
    items = []

    # Files of the same tile, date and band are versions of an acquisition
    files = files.copy()
    files["version"] = files.groupby(["tile", "date", "band"]).cumcount()

    for (tile, date, version), group in files.groupby(
        ["tile", "date", "version"], sort=True
    ):
        crs = str(group["crs"].iloc[0])
        assets = {}

        for _, file in group.iterrows():
            transform = Affine(
                a=float(file["xres"]),
                b=0.0,
                c=float(file["xmin"]),
                d=0.0,
                e=-float(file["yres"]),
                f=float(file["ymax"]),
            )

            # Create asset
            asset = pystac.Asset(
                href=str(file["path"]),
                roles=["data"],
            )

            # Define extra fields
            asset.extra_fields.update(
                {
                    "proj:wkt2": crs,
                    "proj:shape": [int(file["nrows"]), int(file["ncols"])],
                    "proj:transform": [*list(transform)[:6], 0.0, 0.0, 1.0],
                }
            )

            # Save band
            assets[str(file["band"])] = asset

        # Footprint, in geographic coordinates (required by STAC)
        bbox = list(
            transform_bounds(
                src_crs=crs,
                dst_crs="EPSG:4326",
                left=float(group["xmin"].min()),
                bottom=float(group["ymin"].min()),
                right=float(group["xmax"].max()),
                top=float(group["ymax"].max()),
            )
        )

        # Create item
        item = pystac.Item(
            id=f"{tile}_{date}_{version}",
            geometry={
                "type": "Polygon",
                "coordinates": [
                    [
                        [bbox[0], bbox[1]],
                        [bbox[2], bbox[1]],
                        [bbox[2], bbox[3]],
                        [bbox[0], bbox[3]],
                        [bbox[0], bbox[1]],
                    ]
                ],
            },
            bbox=bbox,
            datetime=datetime64(str(date)).astype("datetime64[s]").item(),
            properties={"tile": tile},
        )

        # Add assets
        for band, asset in assets.items():
            item.add_asset(band, asset)

        # Save item
        items.append(item)

    # Return!
    return items


#
# Data access
#
def signature_file_url(url: str) -> str:
    """Refresh the credentials of a file URL.

    Cubes store the credentials available when they were created. As these
    credentials expire, they are refreshed before data is read.

    Args:
        url (str): File URL.

    Returns:
        str: URL with refreshed credentials, if required.
    """
    prefix = VSICURL_PREFIX if url.startswith(VSICURL_PREFIX) else ""
    address = url[len(prefix) :]

    parsed = urlparse(address)

    # Only data with expiring credentials is refreshed
    if not parsed.netloc.endswith(MPC_HOST_SUFFIX) or not parsed.query:
        return url

    try:
        from planetary_computer import sign

    except ImportError:
        return url

    return prefix + sign(urlunparse(parsed._replace(query="")))
