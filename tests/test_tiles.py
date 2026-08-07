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

"""Unit tests for tile-related operations."""

import pytest

from pysits import sits_cube, sits_roi_to_tiles, sits_tiles_to_roi
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.frame import SITSFrameSF
from pysits.models.data.vector import SITSNamedVector


@pytest.mark.parametrize(
    ("grid_system", "expected_tiles"),
    [
        ("MGRS", ["20LLQ", "20LMQ"]),
        ("BDC_MD_V2", ["006007", "006008"]),
    ],
)
def test_roi_to_tiles(grid_system: str, expected_tiles: list[str]):
    """Test ROI to tiles."""
    roi = dict(
        lon_min=-64.037,
        lat_min=-9.644,
        lon_max=-63.886,
        lat_max=-9.389,
    )

    tiles = sits_roi_to_tiles(roi, grid_system=grid_system)

    # Test type
    assert isinstance(tiles, SITSFrameSF)

    # Columns
    assert all(
        x in tiles.columns for x in ["tile_id", "coverage_percentage", "geometry"]
    )

    # Expected tiles
    assert sorted(tiles["tile_id"]) == expected_tiles


@pytest.mark.parametrize(
    ("grid_system", "tiles", "expected_roi"),
    [
        ("MGRS", "22KGA", (-49.067207, -22.683553, -47.985736, -21.676399)),
        ("BDC_MD_V2", "006007", (-64.242845, -9.529926, -62.235677, -7.584190)),
    ],
)
def test_tiles_to_roi(grid_system: str, tiles: str, expected_roi: tuple[float, ...]):
    """Test tiles to ROI."""
    roi = sits_tiles_to_roi(tiles, grid_system=grid_system)

    # Test type
    assert isinstance(roi, SITSNamedVector)

    # Columns
    assert roi.shape == (1, 4)
    assert all(x in roi.columns for x in ["lon_min", "lat_min", "lon_max", "lat_max"])

    # Expected ROI
    assert roi.iloc[0].tolist() == pytest.approx(expected_roi)


def test_tiles_to_load_cube():
    """Test tiles to load cube."""
    # Test new version
    roi = sits_tiles_to_roi("22KGA")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        roi=roi,
        start_date="2020-01-01",
        end_date="2020-02-01",
        progress=False,
    )

    assert isinstance(cube, SITSCubeModel)
    assert cube.tile.iloc[0] == "013011"


def test_roi_to_tiles_to_load_cube():
    """Test ROI tiles to load cube."""
    roi = dict(
        lon_min=-64.037,
        lat_min=-9.644,
        lon_max=-63.886,
        lat_max=-9.389,
    )

    # Find tiles of the ROI
    tiles = sits_roi_to_tiles(roi, grid_system="MGRS")

    # Load cube using the tiles found
    cube = sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        tiles=tiles["tile_id"].tolist(),
        bands=("B02",),
        start_date="2020-01-01",
        end_date="2020-02-01",
        progress=False,
    )

    assert isinstance(cube, SITSCubeModel)
    assert sorted(cube.tile) == ["20LLQ", "20LMQ"]
