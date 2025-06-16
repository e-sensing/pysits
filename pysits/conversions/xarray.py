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

"""Xarray conversions."""

from __future__ import annotations

import dask.array as dask_array
import numpy as np
import rioxarray as xrio
import xarray as xr
from affine import Affine
from pandas import concat as pandas_concat
from pandas import to_datetime as pandas_to_datetime

from pysits.models.data.base import SITSData


#
# Auxiliary functions
#
def _xarray_load_raster(
    raster_path: str, crs: str, shape: tuple[int, int], transform: float
) -> xr.Dataset:
    """Load raster with rio-xarray.

    Args:
        raster_path (str): Complete path to the raster.

        crs (str): Dataset CRS.

        shape (Tuple[int, int]): Dataset shape.

        transform (float): Project transform.

    Returns:
        xr.Dataset: Raster loaded as Dataset
    """
    da = xrio.open_rasterio(raster_path, masked=True)
    da = da.squeeze("band", drop=True)

    return da.rio.reproject(
        dst_crs=crs,
        shape=shape,
        transform=transform,
        resampling=0,  # 0 = Nearest
    )


#
# SITS conversions function
#
def pandas_sits_as_xarray(data: SITSData) -> xr.Dataset:
    """Convert sits to xarray.

    Args:
        data (pysits.models.SITSData): SITS Data.

    Returns:
        xr.Dataset: SITS data as xarray.Dataset.
    """
    # Metadata columns
    time_series_metadata = data.drop(columns="time_series")

    # Extract time-series column
    time_series_data = data["time_series"]

    # Convert to a list of data frames
    time_series_data = time_series_data.tolist()

    # Get time-series attributes (removing ``Index``)
    time_series_attributes = set(time_series_data[0].columns).difference(["Index"])
    time_series_attributes = list(time_series_attributes)

    # Extract samples timeline
    timeline = time_series_data[0]["Index"]

    # Drop ``Index`` and create a stack
    time_series_data = np.stack(
        [ts.drop(columns="Index").to_numpy() for ts in time_series_data]
    )

    # Create xarray dataset
    return xr.Dataset(
        data_vars={
            var: (["sample", "time"], time_series_data[:, :, i])
            for i, var in enumerate(time_series_attributes)
        },
        coords={
            "sample": np.arange(len(time_series_metadata)),
            "time": timeline,
            "longitude": ("sample", time_series_metadata["longitude"].to_numpy()),
            "latitude": ("sample", time_series_metadata["latitude"].to_numpy()),
            "label": ("sample", time_series_metadata["label"].to_numpy()),
            "cube": ("sample", time_series_metadata["cube"].to_numpy()),
        },
    )


def pandas_cube_as_xarray(cube: SITSData) -> xr.Dataset:
    """Convert cube to xarray.

    Args:
        cube (pysits.models.SITSData): Cube data

    Returns:
        xr.Dataset: Cube data as xarray.Dataset.
    """
    # Get all files from the cube
    cube_file_info = cube["file_info"].tolist()

    # Merge and sort values
    cube_file_info = pandas_concat(cube_file_info, ignore_index=True)
    cube_file_info = cube_file_info.sort_values(["date", "band"]).reset_index(drop=True)

    # Assuming all cube have the same CRS / resolution, use one file
    # to extract ``shape``, ``coords`` and ``crs``
    cube_sample = cube_file_info.iloc[0]["path"]

    # Open file
    cube_sample = xrio.open_rasterio(cube_sample, masked=True)

    # Extract info
    cube_crs = cube_sample.rio.crs
    cube_res_x, cube_res_y = list(map(lambda x: abs(x), cube_sample.rio.resolution()))

    # To handle multiple tiles, use a ``global`` extent, covering all tiles
    xmin = cube_file_info["xmin"].min()
    xmax = cube_file_info["xmax"].max()
    ymin = cube_file_info["ymin"].min()
    ymax = cube_file_info["ymax"].max()

    # Calculate global shape
    width = int(np.ceil((xmax - xmin) / cube_res_x))
    height = int(np.ceil((ymax - ymin) / cube_res_y))

    # Define global transform
    global_transform = Affine.translation(xmin, ymax) * Affine.scale(
        cube_res_x, -cube_res_y
    )

    # Define X and Y coordinates
    x_coords = np.arange(width) * cube_res_x + xmin + cube_res_x / 2
    y_coords = ymax - np.arange(height) * cube_res_y - cube_res_y / 2

    # Prepare variables by band and date
    dataset_vars = {}

    for band, band_data in cube_file_info.groupby("band"):
        data_arrays = []
        time_coords = []

        # Sort by date
        band_data_sorted = band_data.sort_values("date")

        # Iterate bands
        for _, row in band_data_sorted.iterrows():
            # Get info
            da_path = row["path"]
            da_date = row["date"]

            # Load raster (band / date)
            da_raster = _xarray_load_raster(
                raster_path=da_path,
                crs=cube_crs,
                shape=(height, width),
                transform=global_transform,
            )

            # Save data
            data_arrays.append(da_raster)
            time_coords.append(da_date)

        # Stack data
        stacked = dask_array.stack(data_arrays, axis=0)

        # Save as variable (all bands in ``time``, ``y`` and ``x``)
        dataset_vars[band] = (("time", "y", "x"), stacked)

    # Build data cube
    ds = xr.Dataset(
        data_vars=dataset_vars,
        coords={
            "time": pandas_to_datetime(time_coords),
            "y": y_coords,
            "x": x_coords,
        },
    )

    # Save CRS
    ds.rio.write_crs(cube_crs, inplace=True)

    return ds
