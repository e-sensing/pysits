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

"""Docs decorators."""

import importlib.resources
from collections.abc import Callable
from typing import ParamSpec, TypeVar

#
# Generics
#
T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


#
# Decorators
#
def attach_doc(name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator that attaches a docstring to a function from a markdown file
    located in the `pysits/docs/` package directory.

    Args:
        name (str): The name of the markdown file (without extension).

    Returns:
        Callable: A decorator that injects the loaded docstring.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        try:
            with (
                importlib.resources.files("pysits.docs.content")
                .joinpath(f"{name}.md")
                .open("r", encoding="utf-8") as f
            ):
                func.__doc__ = f.read()
        except (FileNotFoundError, ModuleNotFoundError):
            func.__doc__ = f"(No documentation found for {name})"
        return func

    return decorator
