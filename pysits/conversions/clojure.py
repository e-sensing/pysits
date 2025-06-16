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

"""Clojure utilities."""

from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import rpy2_fix_type, rpy2_fix_type_custom

#
# Generics
#
R = TypeVar("R")
P = ParamSpec("P")


#
# Factory function
#
def closure_factory(
    name: str, converters: dict[str, Callable[[Any], Any]] = {}
) -> Callable[P, R]:
    """Factory to create sits-based closure functions.

    This function creates a closure that wraps R package sits functions,
    making them callable from Python. It checks if the requested function
    exists in the R sits package before creating the wrapper.

    Args:
        name (str): Name of the sits-based function to be wrapped from the R package.

    Returns:
        Callable[P, R]: A wrapped function that forwards calls to the R sits package.
            The function accepts any arguments (*args, **kwargs) and returns the result
            from the R function.

    Raises:
        ValueError: If the specified function name does not exist in the R sits package.
    """
    if not hasattr(r_pkg_sits, name):
        raise ValueError(f"Invalid function: {name}")

    # define method closure
    @rpy2_fix_type_custom(converters)
    @rpy2_fix_type
    def _fnc(*args: P.args, **kwargs: P.kwargs) -> R:
        return getattr(r_pkg_sits, name)(*args, **kwargs)

    # set function name
    _fnc.__name__ = name

    return _fnc
