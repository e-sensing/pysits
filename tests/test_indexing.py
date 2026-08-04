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

"""Unit tests for indexing operations."""

import numpy as np
import pytest
import rasterio
from affine import Affine
from pandas import Series as PandasSeries
from rasterio.crs import CRS

from pysits.models.data.cube import SITSCubeItemModel, SITSCubeModel
from pysits.models.data.ts import SITSTimeSeriesItemModel, SITSTimeSeriesModel
from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube

#
# Tiles of the cube used to test indexing
#
CUBE_TILES = ("20LLQ", "20LLR")

#
# Grid of the cube used to test indexing
#
CUBE_CRS = "EPSG:32720"
CUBE_SIZE = 50
CUBE_RESOLUTION = 10.0


@pytest.fixture(scope="session")
def cube_dir(tmp_path_factory):
    """Create a directory with files of two tiles."""
    # Create directory
    data_dir = tmp_path_factory.mktemp("cube-tiles")

    # Create a raster file for each tile
    for index, tile in enumerate(CUBE_TILES):
        # Transform matrix for the tile
        transform = Affine(
            a=CUBE_RESOLUTION,
            b=0.0,
            c=300000.0 + index * 100000.0,
            d=0.0,
            e=-CUBE_RESOLUTION,
            f=8000000.0,
        )

        # Create a raster file for each date
        for date in ("2020-01-01", "2020-01-16"):
            # Create a raster file for the date
            with rasterio.open(
                fp=data_dir / f"SENTINEL-2_MSI_{tile}_B02_{date}.tif",
                mode="w",
                driver="GTiff",
                height=CUBE_SIZE,
                width=CUBE_SIZE,
                count=1,
                dtype="int16",
                crs=CRS.from_string(CUBE_CRS),
                transform=transform,
                nodata=-9999,
            ) as dataset:
                dataset.write(np.full((CUBE_SIZE, CUBE_SIZE), index + 1, "int16"), 1)

    return data_dir


@pytest.fixture
def cube(cube_dir):
    """Create a cube with two tiles."""
    return sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        data_dir=cube_dir.as_posix(),
        parse_info=("X1", "X2", "tile", "band", "date"),
        bands="B02",
        progress=False,
    )


def test_cube_indexing(cube):
    """Test cube indexing."""
    assert sorted(cube.tile) == list(CUBE_TILES)

    # Indexing tests
    idx1 = cube[cube["tile"] == "20LLR"]
    assert idx1.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx1.tile.iloc[0] == "20LLR"
    assert idx1._instance is not None
    assert isinstance(idx1, SITSCubeModel)

    idx2 = cube.query("tile == '20LLQ'")
    assert idx2.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx2.tile.iloc[0] == "20LLQ"
    assert idx2._instance is not None
    assert isinstance(idx2, SITSCubeModel)

    idx3 = cube.iloc[0]
    assert idx3.shape[0] == 11  # noqa: PLR2004 - 11 columns
    assert idx3.tile == "20LLQ"
    assert idx3._instance is not None
    assert isinstance(idx3, SITSCubeItemModel)

    idx4 = cube.iloc[0:1,]
    assert idx4.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx4.tile.iloc[0] == "20LLQ"
    assert idx4._instance is not None
    assert isinstance(idx4, SITSCubeModel)

    idx5 = cube.iloc[0:1, 4]
    assert idx5.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx5.iloc[0] == "20LLQ"
    assert isinstance(idx5, PandasSeries)

    idx6 = cube.loc[0]
    assert idx6.shape[0] == 11  # noqa: PLR2004 - 11 columns
    assert idx6.tile == "20LLQ"
    assert idx6._instance is not None
    assert isinstance(idx6, SITSCubeItemModel)

    idx7 = cube.loc[0:1,]
    assert idx7.shape[0] == 2  # noqa: PLR2004 - 2 rows
    assert idx7._instance is not None
    assert isinstance(idx7, SITSCubeModel)

    idx8 = cube.loc[0, "tile"]
    assert idx8 == "20LLQ"

    cols = ["source", "collection", "tile"]
    idx9 = cube[cols]
    assert [col in idx9.columns for col in cols]


def test_cube_indexing_without_results(cube):
    """Test cube indexing when no rows are selected."""
    rows = (cube[cube["tile"] == "does-not-exist"], cube.query("tile == 'none'"))

    for empty in rows:
        # Test types
        assert isinstance(empty, SITSCubeModel)
        assert empty.shape[0] == 0

        # Cube instances are empty
        assert empty._instance is None


def test_ts_indexing():
    """Test time-series indexing."""
    samples = samples_l8_rondonia_2bands

    # Indexing tests
    idx1 = samples[samples["label"] == "Deforestation"]
    assert idx1.shape[0] == 40  # noqa: PLR2004 - 40 rows
    assert all(idx1.label.unique() == "Deforestation")
    assert idx1._instance is not None
    assert isinstance(idx1, SITSTimeSeriesModel)

    idx2 = samples.query("label == 'Pasture'")
    assert idx2.shape[0] == 40  # noqa: PLR2004 - 40 rows
    assert all(idx2.label.unique() == "Pasture")
    assert idx2._instance is not None
    assert isinstance(idx2, SITSTimeSeriesModel)

    idx3 = samples.iloc[0]
    assert idx3.shape[0] == 7  # noqa: PLR2004 - 7 columns
    assert idx3.label == "Deforestation"
    assert idx3._instance is not None
    assert isinstance(idx3, SITSTimeSeriesItemModel)

    idx4 = samples.iloc[0:1,]
    assert idx4.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx4.label.iloc[0] == "Deforestation"
    assert idx4._instance is not None
    assert isinstance(idx4, SITSTimeSeriesModel)

    idx5 = samples.iloc[0:1, 4]
    assert idx5.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx5.iloc[0] == "Deforestation"
    assert isinstance(idx5, PandasSeries)

    idx6 = samples.loc[0]
    assert idx6.shape[0] == 7  # noqa: PLR2004 - 7 columns
    assert idx6.label == "Deforestation"
    assert idx6._instance is not None
    assert isinstance(idx6, SITSTimeSeriesItemModel)

    idx7 = samples.loc[0:1,]
    assert idx7.shape[0] == 2  # noqa: PLR2004 - 1 row
    assert idx7._instance is not None
    assert isinstance(idx7, SITSTimeSeriesModel)

    idx8 = samples.loc[150, "label"]
    assert idx8 == "Pasture"

    cols = ["label", "longitude", "latitude"]
    idx9 = samples[cols]
    assert [col in idx9.columns for col in cols]
