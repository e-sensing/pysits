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

"""Unit tests for the conversions module."""

import pytest
import rpy2.robjects as ro
from geopandas import GeoDataFrame
from pandas import DataFrame as PandasDataFrame
from shapely.geometry import Point

from pysits.conversions.clojure import closure_factory
from pysits.conversions.common import (
    convert_dict_like_as_list_to_r,
    convert_dict_like_to_r,
    convert_list_like_to_r,
    convert_to_python,
)
from pysits.conversions.tibble import (
    _column_to_datetime,
    geopandas_to_tibble,
    pandas_cube_to_tibble,
    pandas_sits_to_tibble,
    pandas_to_tibble,
    tibble_nested_to_pandas,
)
from pysits.conversions.vector import matrix_to_pandas, table_to_pandas
from pysits.models.frame import NestedFrame
from pysits.sits.context import samples_modis_ndvi


def test_closure_factory_invalid_function():
    """Test that closure_factory raises ValueError for invalid function names."""
    with pytest.raises(ValueError) as exc_info:
        closure_factory("non_existent_function")

    assert str(exc_info.value) == "Invalid function: non_existent_function"


def test_convert_list_like_to_r():
    """Test conversion of Python list-like objects to R vectors."""
    # Test integer list
    int_list = [1, 2, 3, 4, 5]
    int_result = convert_list_like_to_r(int_list)
    assert isinstance(int_result, ro.vectors.IntVector)
    assert list(int_result) == int_list

    # Test float list
    float_list = [1.1, 2.2, 3.3, 4.4, 5.5]
    float_result = convert_list_like_to_r(float_list)
    assert isinstance(float_result, ro.vectors.FloatVector)
    assert list(float_result) == float_list

    # Test int + float list
    mixed_list = [1, 2.2, 3, 4.4, 5]
    mixed_result = convert_list_like_to_r(mixed_list)
    assert isinstance(mixed_result, ro.vectors.FloatVector)
    assert list(mixed_result) == mixed_list

    # Test string list
    str_list = ["a", "b", "c", "d"]
    str_result = convert_list_like_to_r(str_list)
    assert isinstance(str_result, ro.vectors.StrVector)
    assert list(str_result) == str_list

    # Test boolean list
    bool_list = [True, False, True, True]
    bool_result = convert_list_like_to_r(bool_list)
    assert isinstance(bool_result, ro.vectors.IntVector)
    assert list(bool_result) == bool_list

    # Test mixed type list
    mixed_list = [1, "text", 3.14, True]
    mixed_result = convert_list_like_to_r(mixed_list)
    assert isinstance(mixed_result, ro.vectors.ListVector)
    # Check that keys are string indices
    assert list(mixed_result.names) == ["0", "1", "2", "3"]
    # Check values are correctly converted
    assert isinstance(mixed_result[0], ro.vectors.IntVector)
    assert isinstance(mixed_result[1], ro.vectors.StrVector)
    assert isinstance(mixed_result[2], ro.vectors.FloatVector)
    assert isinstance(mixed_result[3], ro.vectors.BoolVector)


def test_convert_dict_like_to_r():
    """Test conversion of Python dictionaries to R vectors."""
    # Test dictionary with all string values -> StrVector
    str_dict = {"a": "apple", "b": "banana", "c": "cherry"}
    str_result = convert_dict_like_to_r(str_dict)
    assert isinstance(str_result, ro.vectors.StrVector)
    assert list(str_result.names) == ["a", "b", "c"]
    assert list(str_result) == ["apple", "banana", "cherry"]

    # Empty dictionary
    empty_result = convert_dict_like_to_r({})
    assert isinstance(empty_result, ro.vectors.ListVector)

    # Test dictionary with mixed value types -> ListVector
    mixed_dict = {
        "int": 42,
        "float": 3.14,
        "str": "hello",
        "bool": True,
        "list": [1, 2, 3],
        "mixed": [1, "text", 3.14, True],
        "empty": [],
        "numeric": [1, 2.2, 3, 4.44],
    }
    mixed_result = convert_dict_like_to_r(mixed_dict)
    assert isinstance(mixed_result, ro.vectors.ListVector)
    assert list(mixed_result.names) == [
        "int",
        "float",
        "str",
        "bool",
        "list",
        "mixed",
        "empty",
        "numeric",
    ]

    # Check individual value types and conversions
    assert isinstance(mixed_result[0], ro.vectors.IntVector)
    assert list(mixed_result[0]) == [42]

    assert isinstance(mixed_result[1], ro.vectors.FloatVector)
    assert list(mixed_result[1]) == [3.14]

    assert isinstance(mixed_result[2], ro.vectors.StrVector)
    assert list(mixed_result[2]) == ["hello"]

    assert isinstance(mixed_result[3], ro.vectors.BoolVector)
    assert list(mixed_result[3]) == [True]

    assert isinstance(mixed_result[4], ro.vectors.IntVector)
    assert list(mixed_result[4]) == [1, 2, 3]

    assert isinstance(mixed_result[5], ro.vectors.ListVector)
    assert list(mixed_result[5].names) == ["0", "1", "2", "3"]
    assert list(mixed_result[5][0]) == [1]
    assert list(mixed_result[5][1]) == ["text"]
    assert list(mixed_result[5][2]) == [3.14]
    assert list(mixed_result[5][3]) == [True]

    assert isinstance(mixed_result[6], ro.vectors.ListVector)
    assert list(mixed_result[6]) == []

    assert isinstance(mixed_result[7], ro.vectors.FloatVector)
    assert list(mixed_result[7]) == [1, 2.2, 3, 4.44]


def test_convert_dict_like_as_list_to_r():
    """Test conversion of Python dictionaries to R vectors."""
    # Base test case
    data = {"a": "apple", "b": "banana", "c": "cherry"}
    result = convert_dict_like_as_list_to_r(data)

    # Check type
    assert isinstance(result, ro.vectors.ListVector)

    # Check names
    assert list(result.names) == ["a", "b", "c"]

    # Empty dictionary
    empty_result = convert_dict_like_as_list_to_r({})
    assert isinstance(empty_result, ro.vectors.ListVector)


def test_convert_to_python_r_language():
    """Test conversion of unevaluated R expressions."""
    # R expression (e.g., as returned by ``sits_tuning`` hyper-parameters)
    result = convert_to_python(ro.r("quote(c(256, 256, 256))"), as_type="float")

    assert result == [256.0, 256.0, 256.0]

    # R expression nested in a list (e.g., ``opt_hparams``)
    nested_result = convert_to_python(
        ro.r("list(lr = 0.001, betas = quote(c(0.9, 0.999)))"), as_type="float"
    )

    assert nested_result == [{"lr": [0.001]}, {"betas": [0.9, 0.999]}]


def test_matrix_to_pandas():
    """Test conversion of a named R matrix."""
    matrix = ro.r('matrix(1:4, nrow = 2, dimnames = list(c("a", "b"), c("x", "y")))')
    result = matrix_to_pandas(matrix)

    assert result.index.tolist() == ["a", "b"]
    assert result.columns.tolist() == ["x", "y"]
    assert result["x"].tolist() == [1, 2]
    assert result["y"].tolist() == [3, 4]

    # Matrices holding vectors have their single-element cells unwrapped
    list_matrix = ro.r(
        'matrix(list(1, 2, 3, 4), nrow = 2, dimnames = list(c("a", "b"), c("x", "y")))'
    )

    assert matrix_to_pandas(list_matrix)["x"].tolist() == [1.0, 2.0]


def test_table_to_pandas():
    """Test conversion of 1D and 2D R tables."""
    # 1D table
    result_1d = table_to_pandas(ro.r('table(factor(c("a", "b", "a")))'))

    assert result_1d.index.tolist() == ["a", "b"]
    assert result_1d.iloc[:, 0].tolist() == [2, 1]

    # 2D table
    result_2d = table_to_pandas(ro.r('table(factor(c("a", "b")), factor(c("x", "x")))'))

    assert result_2d.index.tolist() == ["a", "b"]
    assert result_2d.columns.tolist() == ["x"]

    # Tables with more than two dimensions are not supported
    with pytest.raises(ValueError, match="Only 1D and 2D tables"):
        table_to_pandas(
            ro.r('table(factor("a"), factor("b"), factor("c"))'),
        )


def test_column_to_datetime():
    """Test conversion of R date offsets to datetime columns."""
    data = _column_to_datetime(PandasDataFrame({"start_date": [0, 366]}), "start_date")

    assert data["start_date"].dt.strftime("%Y-%m-%d").tolist() == [
        "1970-01-01",
        "1971-01-02",
    ]

    # Missing columns are ignored
    assert "end_date" not in _column_to_datetime(data, "end_date").columns


def test_pandas_to_tibble():
    """Test conversion of a pandas DataFrame to an R data frame."""
    result = pandas_to_tibble(PandasDataFrame({"a": [1, 2], "b": ["x", "y"]}))

    assert isinstance(result, ro.vectors.DataFrame)
    assert list(result.colnames) == ["a", "b"]


def test_tibble_nested_to_pandas():
    """Test conversion of an R tibble with nested data frames."""
    data = ro.r("tibble::tibble(id = 1L, ts = list(tibble::tibble(v = c(1, 2))))")
    result = tibble_nested_to_pandas(data, nested_columns=["ts"])

    assert result["id"].tolist() == [1]
    assert isinstance(result["ts"][0], NestedFrame)
    assert result["ts"][0]["v"].tolist() == [1.0, 2.0]

    # Nested frames are shown as a compact summary
    assert repr(result["ts"][0]) == "NestedFrame(2 x 1)"


def test_geopandas_to_tibble():
    """Test conversion of a GeoDataFrame to an R sf object."""
    data = GeoDataFrame(
        data={"a": [1]},
        geometry=[Point(0, 0)],
        crs="EPSG:4326",
    )
    result = geopandas_to_tibble(data)

    assert "sf" in list(ro.r["class"](result))
    assert "a" in list(ro.r["names"](result))


def test_geopandas_to_tibble_without_crs():
    """Test conversion of a GeoDataFrame without CRS."""
    data = GeoDataFrame(
        data={"a": [1]},
        geometry=[Point(0, 0)],
    )

    with pytest.raises(ValueError, match="must have a CRS"):
        geopandas_to_tibble(data)


def test_geopandas_to_tibble_with_nested_columns():
    """Test conversion of a GeoDataFrame with embedded DataFrames."""
    data = GeoDataFrame(
        data={"a": [1], "nested": [PandasDataFrame({"v": [1]})]},
        geometry=[Point(0, 0)],
        crs="EPSG:4326",
    )

    with pytest.warns(UserWarning, match="Dropping columns with embedded DataFrames"):
        result = geopandas_to_tibble(data)

    assert "nested" not in list(ro.r["names"](result))


def test_pandas_sits_to_tibble():
    """Test conversion of a sits pandas DataFrame to an R tibble."""
    data = PandasDataFrame(samples_modis_ndvi.head(2)).copy()
    result = pandas_sits_to_tibble(data)

    assert list(result.rclass) == ["sits", "tbl_df", "tbl", "data.frame"]

    # Optional columns define additional classes
    data["predicted"] = data["time_series"]
    data["base_data"] = data["time_series"]
    data["id_sample"] = [1, 2]
    data["id_neuron"] = [1, 2]

    rclass = list(pandas_sits_to_tibble(data).rclass)

    assert "predicted" in rclass
    assert "sits_base" in rclass
    assert "som_clean_samples" in rclass


def test_pandas_cube_to_tibble_empty():
    """Test conversion of a cube pandas DataFrame without tiles."""
    with pytest.raises(ValueError, match="at least one tile"):
        pandas_cube_to_tibble(PandasDataFrame())
