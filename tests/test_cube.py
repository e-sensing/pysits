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

"""Unit tests for cube operations."""

from pysits.models import SITSCubeModel, SITSFrame
from pysits.sits.cube import sits_cube
from pysits.sits.data import sits_bands, sits_bbox, sits_timeline


def test_sits_cube_data_structure():
    """Test data structure of sits_cube."""
    # Define a region of interest for the city of Sinop
    roi_sinop = {
        "lon_min": -56.87417,
        "lon_max": -54.63718,
        "lat_min": -12.17083,
        "lat_max": -11.02292,
    }

    # Call sits_cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        bands=["NDVI", "EVI"],
        roi=roi_sinop,
        start_date="2013-09-14",
        end_date="2014-08-29",
        progress=False,
    )

    # Verify the result is a SITSCubeModel
    assert isinstance(cube, SITSCubeModel)

    # Check columns
    assert all(
        col in cube.columns
        for col in [
            "source",
            "collection",
            "satellite",
            "sensor",
            "tile",
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "crs",
            "file_info",
        ]
    )

    # Check bands
    cube_bands = sits_bands(cube)
    assert all(band in cube_bands for band in ["NDVI", "EVI"])

    # Check timeline
    cube_timeline = sits_timeline(cube)
    assert len(cube_timeline) == 23  # noqa: PLR2004


def test_sits_cube_bbox():
    """Test bbox of sits cube."""
    # Define a region of interest for the city of Sinop
    roi_sinop = {
        "lon_min": -56.87417,
        "lon_max": -54.63718,
        "lat_min": -12.17083,
        "lat_max": -11.02292,
    }

    # Create a cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        bands=["NDVI", "EVI"],
        roi=roi_sinop,
        start_date="2013-09-14",
        end_date="2014-08-29",
        progress=False,
    )

    # Get bbox
    bbox = sits_bbox(cube)

    # Check bbox structure
    assert isinstance(bbox, SITSFrame)
    assert all(col in bbox.columns for col in ["xmin", "xmax", "ymin", "ymax"])

    # Check crs transformation
    bbox_4326 = sits_bbox(cube, as_crs="EPSG:4326")
    bbox_4326 = bbox_4326.iloc[0]

    assert round(bbox_4326["xmin"], 4) == -63.8507  # noqa: PLR2004
    assert round(bbox_4326["xmax"], 4) == -50.7713  # noqa: PLR2004
    assert round(bbox_4326["ymin"], 4) == -20.0  # noqa: PLR2004
    assert round(bbox_4326["ymax"], 4) == -10.0  # noqa: PLR2004
    assert bbox_4326["crs"] == "EPSG:4326"
