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

"""Unit tests for xarray export operations."""

import xarray as xr

from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube
from pysits.sits.exporters.xarray import sits_as_xarray
from pysits.sits.utils import r_package_dir


def test_xarray_cube_conversion():
    """Test xarray cube conversion."""
    # Create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir,
    )

    xcube = sits_as_xarray(cube)

    assert isinstance(xcube, xr.Dataset)
    assert xcube.time.size == 12  # noqa: PLR2004
    assert "NDVI" in xcube


def test_xarray_sits_conversion():
    """Test xarray sits conversion."""
    xsamples_ts = sits_as_xarray(samples_l8_rondonia_2bands)

    assert "EVI" in xsamples_ts
    assert "NDVI" in xsamples_ts
    assert xsamples_ts.time.size == 25  # noqa: PLR2004
    assert isinstance(xsamples_ts, xr.Dataset)
