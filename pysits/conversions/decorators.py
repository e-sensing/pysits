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

"""Decorators."""

import functools
import inspect
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from pysits.conversions.common import convert_to_r, fix_reserved_words_parameters

#
# Generics
#
T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


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
        kwargs = fix_reserved_words_parameters(**kwargs)
        converted_args = [convert_to_r(arg) for arg in args]
        converted_kwargs = {k: convert_to_r(v) for k, v in kwargs.items()}
        return func(*converted_args, **converted_kwargs)

    return wrapper


def rpy2_fix_type_custom(
    converters: dict[str, Callable[[Any], Any]],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Convert arguments to R objects using parameter-specific converters.

    Args:
        converters (dict[str, Callable[[Any], Any]]): A dictionary mapping
            parameter names to converter functions. Each converter function should
            take a Python object and return an R-compatible object. Parameters not
            found in this dictionary will be passed as is.

    Returns:
        Callable: A decorator that wraps a function to convert its arguments using the
                  parameter-specific converters.

    Example:
        >>> converters = {
        ...     "optimizer": convert_optimizer,
        ...     "opt_hparams": convert_opt_hparams
        ... }
        >>> @rpy2_fix_type_custom(converters)
        ... def my_function(optimizer, opt_hparams, other_arg):
        ...     # optimizer and opt_hparams will use their specific converters
        ...     # other_arg will use the default _convert_to_r
        ...     pass
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get the function's parameter names
            param_names = inspect.signature(func).parameters.keys()
            param_names = list(param_names)

            # Convert positional arguments using their parameter names
            converted_args = []
            for i, arg in enumerate(args):
                if i < len(param_names) and param_names[i] in converters:
                    converted_args.append(converters[param_names[i]](arg))
                else:
                    converted_args.append(arg)

            # Convert keyword arguments
            converted_kwargs = {}
            for k, v in kwargs.items():
                if k in converters:
                    converted_kwargs[k] = converters[k](v)
                else:
                    converted_kwargs[k] = v

            return func(*converted_args, **converted_kwargs)

        return wrapper

    return decorator


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
