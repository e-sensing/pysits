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

from pandas import Series as PandasSeries

from pysits.models.data.cube import SITSCubeItemModel, SITSCubeModel
from pysits.models.data.ts import SITSTimeSeriesItemModel, SITSTimeSeriesModel
from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube


def test_cube_indexing():
    """Test cube indexing."""
    cbers_tile = sits_cube(
        source="BDC",
        collection="CBERS-WFI-16D",
        bands=("NDVI", "EVI"),
        tiles=("007004", "007005"),
        start_date="2018-09-01",
        end_date="2019-08-28",
    )

    # Indexing tests
    idx1 = cbers_tile[cbers_tile["tile"] == "007005"]
    assert idx1.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx1.tile.iloc[0] == "007005"
    assert idx1._instance is not None
    assert isinstance(idx1, SITSCubeModel)

    idx2 = cbers_tile.query("tile == '007004'")
    assert idx2.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx2.tile.iloc[0] == "007004"
    assert idx2._instance is not None
    assert isinstance(idx2, SITSCubeModel)

    idx3 = cbers_tile.iloc[0]
    assert idx3.shape[0] == 11  # noqa: PLR2004 - 11 columns
    assert idx3.tile == "007004"
    assert idx3._instance is not None
    assert isinstance(idx3, SITSCubeItemModel)

    idx4 = cbers_tile.iloc[0:1,]
    assert idx4.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx4.tile.iloc[0] == "007004"
    assert idx4._instance is not None
    assert isinstance(idx4, SITSCubeModel)

    idx5 = cbers_tile.iloc[0:1, 4]
    assert idx5.shape[0] == 1  # noqa: PLR2004 - 1 row
    assert idx5.iloc[0] == "007004"
    assert isinstance(idx5, PandasSeries)

    idx6 = cbers_tile.loc[0]
    assert idx6.shape[0] == 11  # noqa: PLR2004 - 11 columns
    assert idx6.tile == "007004"
    assert idx6._instance is not None
    assert isinstance(idx6, SITSCubeItemModel)

    idx7 = cbers_tile.loc[0:1,]
    assert idx7.shape[0] == 2  # noqa: PLR2004 - 1 row
    assert idx7._instance is not None
    assert isinstance(idx7, SITSCubeModel)

    idx8 = cbers_tile.loc[0, "tile"]
    assert idx8 == "007004"

    cols = ["source", "collection", "tile"]
    idx9 = cbers_tile[cols]
    assert [col in idx9.columns for col in cols]


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
