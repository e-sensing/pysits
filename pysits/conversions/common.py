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

"""Common conversions."""

from datetime import date, timedelta
from pathlib import Path, PosixPath

import rpy2.robjects as ro
from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from rpy2.rinterface_lib.sexp import NULLType
from rpy2.robjects import pandas2ri
from rpy2.robjects.robject import RObjectMixin

from pysits.backend.pkgs import r_pkg_tibble
from pysits.conversions.dsl.base import DSLObject
from pysits.conversions.tibble import geopandas_to_tibble, pandas_to_tibble

#
# Type mapping dictionary
#
TYPE_CONVERSIONS = {
    list: lambda obj: convert_list_like_to_r(obj),
    tuple: lambda obj: convert_list_like_to_r(obj),
    set: lambda obj: convert_list_like_to_r(list(obj)),
    dict: lambda obj: convert_dict_like_to_r(obj),
    bool: lambda obj: ro.BoolVector([obj]),
    int: lambda obj: ro.IntVector([obj]),
    float: lambda obj: ro.FloatVector([obj]),
    str: lambda obj: ro.StrVector([obj]),
    Path: lambda obj: ro.StrVector([obj.as_posix()]),
    PosixPath: lambda obj: ro.StrVector([obj.as_posix()]),
    PandasDataFrame: lambda obj: r_pkg_tibble.as_tibble(pandas_to_tibble(obj)),
    GeoPandasDataFrame: lambda obj: geopandas_to_tibble(obj),
}


#
# R epoch reference
#
EPOCH_START = date(1970, 1, 1)


#
# Base utilities
#
def _is_numeric(x: int | float) -> bool:
    """Helper function to check if a value is numeric (int or float)."""
    return isinstance(x, int | float)


#
# Base conversions
#
def convert_list_like_to_r(obj: list | tuple | set) -> ro.vectors.Vector:  # noqa: PLR0911
    """
    Converts a list-like object to the appropriate R vector type.

    Args:
        obj (list, tuple, set): The list-like Python object.

    Returns:
        An R-compatible vector.
    """
    if not obj:
        return ro.vectors.ListVector({})

    if all(isinstance(x, int) for x in obj):
        return ro.vectors.IntVector(obj)

    elif all(isinstance(x, float) for x in obj):
        return ro.vectors.FloatVector(obj)

    # Check if all elements are numeric (int or float)
    elif all(_is_numeric(x) for x in obj):
        return ro.vectors.FloatVector(obj)

    elif all(isinstance(x, str) for x in obj):
        return ro.vectors.StrVector(obj)

    elif all(isinstance(x, bool) for x in obj):
        return ro.BoolVector(obj)

    else:
        return ro.vectors.ListVector(
            {str(i): convert_to_r(v) for i, v in enumerate(obj)}
        )


def convert_dict_like_as_list_to_r(obj: dict) -> ro.vectors.ListVector:
    """Convert a Python dict to a ListVector."""
    return ro.vectors.ListVector({str(k): convert_to_r(v) for k, v in obj.items()})


def convert_dict_like_to_r(obj: dict) -> ro.vectors.Vector:
    """Convert a Python dictionary to an R vector.

    This function converts a Python dictionary to either a typed R vector or ListVector,
    depending on the types of values in the dictionary:
    - If all values are of the same type (e.g. all strings, all numeric), returns an
      appropriate typed R vector with named elements
    - Otherwise, returns an R ListVector with converted values

    Args:
        obj (dict): A Python dictionary to convert to an R vector.

    Returns:
        ro.vectors.Vector: Either a typed R vector (if all values are of same type) or
            an R ListVector (for mixed value types). The resulting vector will
            preserve the dictionary's keys as names in the R vector.
    """
    values = list(obj.values())
    if not values:
        return ro.vectors.ListVector({})

    # Get data properties
    has_unique_type = len(set(type(v) for v in values)) == 1
    is_numeric = all(_is_numeric(v) for v in values)

    # Handle homogeneous data
    if has_unique_type or is_numeric:
        vec = convert_list_like_to_r(values)
        vec.names = list(obj.keys())

        return vec

    # For mixed data, use a list vector
    return convert_dict_like_as_list_to_r(obj)


def convert_to_r(obj):
    """Convert Python objects to R-compatible objects for use with rpy2.

    Args:
        obj: The Python object to convert.

    Returns:
        An R-compatible object.

    Raises:
        TypeError: If the object type cannot be converted.
    """
    if obj is None:
        return ro.r("NULL")  # Convert None to R's NULL

    obj_type = type(obj)

    # Handle ``SITSBase`` objects
    if getattr(obj, "_instance", None):
        # Sync instance with R
        if getattr(obj, "_sync_instance", None):
            obj._sync_instance()

        return obj._instance

    # Handle ``raw R`` / Expressions objects
    if isinstance(obj, RObjectMixin | DSLObject):
        return obj

    # Check if the object type exists in the conversion dictionary
    if obj_type in TYPE_CONVERSIONS:
        return TYPE_CONVERSIONS[obj_type](obj)

    raise TypeError(f"Cannot convert object of type {obj_type} to R format")


def convert_to_python(obj, as_type="str"):
    """Convert an R object to a Python representation.

    Args:
        obj (ro.Vector): The R object to convert.

        as_type (str): The target Python type. Supported values:
            - ``str``: Converts R string vector to Python list of strings;

            - ``date``: Converts R DateVector to list of YYYY-MM-DD formatted strings;

            - ``int``: Converts R numeric vector to Python list of integers;

            - ``float``: Converts R numeric vector to Python list of floats;

            - ``bool``: Converts R logical vector to Python list of booleans.

    Returns:
        list: Converted values as a Python list.

    Raises:
        ValueError: If the specified ``as_type`` is not supported.
    """

    def _convert(value, type_):
        result = []

        if isinstance(value, ro.ListVector):
            for k, v in value.items():
                result.append(
                    {
                        str(k): convert_to_python(v, type_),
                    }
                )

        elif as_type and isinstance(value, ro.Vector):
            for el in value:
                if as_type == "str":
                    result.append(str(el))

                elif as_type == "date":
                    result.append(
                        (EPOCH_START + timedelta(days=int(el))).strftime("%Y-%m-%d")
                    )

                elif as_type == "int":
                    result.append(int(el))

                elif as_type == "float":
                    result.append(float(el))

                elif as_type == "bool":
                    result.append(bool(el))

        elif isinstance(value, ro.Vector):
            result = pandas2ri.rpy2py(value)
            names = value.names

            if not isinstance(names, NULLType):
                result = {str(k): v for k, v in zip(names, result)}

        return result

    return _convert(obj, as_type)


#
# Parameters conversions
#
def fix_reserved_words_parameters(**kwargs) -> dict:
    """Fix reserved words parameters.

    Args:
        **kwargs: The keyword arguments to fix.

    Returns:
        dict: The fixed keyword arguments.
    """
    new_values = {}
    keys_to_remove = []

    for key, _ in kwargs.items():
        # Assuming all reserved words end with "_"
        if key.endswith("_"):
            # Save key to remove
            keys_to_remove.append(key)

            # Save new value
            new_values[key[:-1]] = kwargs[key]

    # Remove keys that were converted
    for key in keys_to_remove:
        kwargs.pop(key)

    # Add remaining kwargs
    if new_values:
        kwargs.update(new_values)

    return kwargs
