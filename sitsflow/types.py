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

import functools
from datetime import date, timedelta

import rpy2.robjects as ro

from sitsflow.models.base import SITSModel

#
# Type mapping dictionary
#
TYPE_CONVERSIONS = {
    list: lambda obj: _convert_list_like(obj),
    tuple: lambda obj: _convert_list_like(obj),
    set: lambda obj: _convert_list_like(list(obj)),
    dict: lambda obj: ro.vectors.ListVector(
        {str(k): _convert_to_r(v) for k, v in obj.items()}
    ),
    bool: lambda obj: ro.BoolVector([obj]),
    int: lambda obj: ro.IntVector([obj]),
    float: lambda obj: ro.FloatVector([obj]),
    str: lambda obj: ro.StrVector([obj]),
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

    # Handle ``SITSModel`` objects
    if isinstance(obj, SITSModel):
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
def rpy2_fix_type(func):
    """Decorator that automatically converts function arguments to R-compatible objects.

    Args:
        func: The function whose arguments should be converted.

    Returns:
        A wrapped function that receives converted arguments.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        converted_args = [_convert_to_r(arg) for arg in args]
        converted_kwargs = {k: _convert_to_r(v) for k, v in kwargs.items()}
        return func(*converted_args, **converted_kwargs)

    return wrapper
