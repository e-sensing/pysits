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

"""Unit tests for geopandas operations."""

from geopandas import GeoDataFrame as GeoPandasDataFrame

from pysits.models.data.frame import SITSFrameSF
from pysits.models.data.ts import SITSTimeSeriesSFModel
from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube
from pysits.sits.exporters import sits_as_geopandas
from pysits.sits.utils import r_package_dir


def test_cube_geopandas_export():
    """Test cube as geopandas."""
    # Load cube
    data_dir = r_package_dir(
        "extdata/raster/mod13q1",
        package="sits",
    )
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir,
    )

    # Export data
    cube_gdf = sits_as_geopandas(cube)

    # Check properties
    assert cube_gdf.crs is not None
    assert cube_gdf.geometry.name == "geometry"
    assert isinstance(cube_gdf, SITSFrameSF)
    assert isinstance(cube_gdf, GeoPandasDataFrame)


def test_ts_geopandas_export():
    """Test time-series data as geopandas."""
    # Export data
    samples_gdf = sits_as_geopandas(samples_l8_rondonia_2bands)

    # Check properties
    assert samples_gdf.crs is not None
    assert samples_gdf.geometry.name == "geometry"
    assert isinstance(samples_gdf, SITSTimeSeriesSFModel)
    assert isinstance(samples_gdf, GeoPandasDataFrame)
