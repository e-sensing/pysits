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

"""Base type conversions."""

import functools
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path, PosixPath
from typing import Any, ParamSpec, TypeVar

import rpy2.robjects as ro
from pandas import DataFrame as PandasDataFrame

from pysits.backend.pkgs import r_pkg_tibble
from pysits.conversions.pandasr import pandas_to_r

#
# Generics
#
T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

#
# Type mapping dictionary
#
TYPE_CONVERSIONS = {
    list: lambda obj: _convert_list_like(obj),
    tuple: lambda obj: _convert_list_like(obj),
    set: lambda obj: _convert_list_like(list(obj)),
    dict: lambda obj: _convert_dict_like(obj),
    bool: lambda obj: ro.BoolVector([obj]),
    int: lambda obj: ro.IntVector([obj]),
    float: lambda obj: ro.FloatVector([obj]),
    str: lambda obj: ro.StrVector([obj]),
    Path: lambda obj: ro.StrVector([obj.as_posix()]),
    PosixPath: lambda obj: ro.StrVector([obj.as_posix()]),
    PandasDataFrame: lambda obj: r_pkg_tibble.as_tibble(pandas_to_r(obj)),
}


#
# Epoch reference (useful for date convertion)
#
EPOCH_START = date(1970, 1, 1)


#
# Type mapping utilities
#
def _convert_list_like(obj):
    """
    Converts a list-like object to the appropriate R vector type.

    Args:
        obj (list, tuple, set): The list-like Python object.

    Returns:
        An R-compatible vector.
    """
    if all(isinstance(x, int) for x in obj):
        return ro.vectors.IntVector(obj)

    elif all(isinstance(x, float) for x in obj):
        return ro.vectors.FloatVector(obj)

    elif all(isinstance(x, str) for x in obj):
        return ro.vectors.StrVector(obj)

    elif all(isinstance(x, bool) for x in obj):
        return ro.BoolVector(obj)

    else:
        return ro.vectors.ListVector(
            {str(i): _convert_to_r(v) for i, v in enumerate(obj)}
        )


def _convert_dict_like(obj: dict) -> ro.vectors.Vector:
    """Convert a Python dictionary to an appropriate R vector type.

    This function converts a Python dictionary to either an R StrVector or ListVector,
    depending on the types of values in the dictionary:
    - If all values are strings, returns an R StrVector with named elements
    - Otherwise, returns an R ListVector with converted values

    Args:
        obj (dict): A Python dictionary to convert to an R vector.

    Returns:
        ro.vectors.Vector: Either an R StrVector (if all values are strings) or
            an R ListVector (for mixed value types). The resulting vector will
            preserve the dictionary's keys as names in the R vector.
    """
    vec = None

    # Assuming str vector for when all values are strings (e.g. label vector)
    if all(isinstance(v, str) for v in obj.values()):
        vec = ro.vectors.StrVector(list(obj.values()))
        vec.names = list(obj.keys())

    # Otherwise, use a list vector
    else:
        vec = ro.vectors.ListVector({str(k): _convert_to_r(v) for k, v in obj.items()})

    return vec


def _convert_to_r(obj):
    """Converts Python objects to R-compatible objects for use with rpy2.

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
        return obj._instance

    # Handle ``closure`` objects
    if isinstance(
        obj,
        (ro.functions.SignatureTranslatedFunction | ro.functions.DocumentedSTFunction),
    ):
        return obj

    # Check if the object type exists in the conversion dictionary
    if obj_type in TYPE_CONVERSIONS:
        return TYPE_CONVERSIONS[obj_type](obj)

    raise TypeError(f"Cannot convert object of type {obj_type} to R format")


#
# Public utility
#
def r_to_python(obj, as_type="str"):
    """Converts an R object to a Python representation.

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
                        str(k): r_to_python(v, type_),
                    }
                )

        elif isinstance(value, ro.Vector):
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

        return result

    return _convert(obj, as_type)


#
# Decorator
#
def rpy2_fix_type(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator function to convert arguments to R-compatible objects.

    Args:
        func (Callable): The function whose arguments should be converted.

    Returns:
        Callable: A wrapped function that receives converted arguments.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        converted_args = [_convert_to_r(arg) for arg in args]
        converted_kwargs = {k: _convert_to_r(v) for k, v in kwargs.items()}
        return func(*converted_args, **converted_kwargs)

    return wrapper


def function_call(r_function: Callable[P, R], output_wrapper: Callable[[R], T]):
    """Decorator function to call an R function and post-process the result.

    This decorator is used to wrap Python stub functions that serve as documentation
    and type hint shells. The resulting function performs the following steps:

    1. Converts all arguments to R-compatible types using `@rpy2_fix_type`.
    2. Calls the provided R function (`r_function`) with converted arguments.
    3. Wraps the result in a specified output Python class (`output_wrapper`).

    This enables consistent logic while preserving per-function docstrings and
    type hints for IDE support, autocompletion, and documentation generation.

    Args:
        r_function (Callable): The R function to be called via rpy2.

        output_wrapper (Callable): A callable (usually a class) that wraps the
                                   result returned by the R function.

    Returns:
        Callable: A decorator that wraps a Python function stub, providing the
                    R execution logic.
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @rpy2_fix_type
        @functools.wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            result = r_function(*args, **kwargs)
            return output_wrapper(result)

        return wrapped

    return decorator
