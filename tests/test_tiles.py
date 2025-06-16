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

from pysits import sits_cube, sits_mgrs_to_roi, sits_tiles_to_roi
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.vector import SITSNamedVector


def test_tiles_to_roi():
    """Test tiles to ROI."""
    # Test new version
    roi = sits_tiles_to_roi("22KGA")

    assert roi.shape == (1, 4)
    assert isinstance(roi, SITSNamedVector)
    assert all(x in roi.columns for x in ["xmin", "xmax", "ymin", "ymax"])

    # Test deprecated version
    roi2 = sits_mgrs_to_roi("20LMM")

    assert roi2.shape == (1, 4)
    assert isinstance(roi2, SITSNamedVector)
    assert all(x in roi2.columns for x in ["xmin", "xmax", "ymin", "ymax"])


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
