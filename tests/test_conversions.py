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

from pysits.conversions.clojure import closure_factory
from pysits.conversions.common import (
    convert_dict_like_as_list_to_r,
    convert_dict_like_to_r,
    convert_list_like_to_r,
)


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
