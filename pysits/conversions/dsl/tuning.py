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

"""DSL for tuning operations."""

from typing import Any

from pysits.conversions.dsl.base import RExpression


class TuningExpression(RExpression):
    """Tuning expression class."""


class TuningSymbol(TuningExpression):
    """Represents an R symbol (variable or function name)."""

    def __init__(self, name: str) -> None:
        """Initializer."""
        self.name = name

    def r_repr(self) -> str:
        """Convert the symbol to its R representation."""
        return self.name


class TuningFunctionCall(TuningExpression):
    """Represents an R function call."""

    def __init__(self, func: str, *args: Any, **kwargs: Any) -> None:
        """Initialize an R function call.

        Args:
            func: The name of the R function to call.

            *args: Positional arguments for the function call.

            **kwargs: Keyword arguments for the function call.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def _convert_arg(self, arg: Any) -> str:
        """Convert a Python argument to its R representation.

        Args:
            arg: The argument to convert. Can be an RExpr, dict, str, bool, None,
                 or any other type that can be converted to string.

        Returns:
            str: The R code string representation of the argument.
        """

        def _convert_dict(d: dict) -> str:
            items = [f"{key} = {self._convert_arg(val)}" for key, val in d.items()]
            return f"list({', '.join(items)})"

        def _convert_string(s: str) -> str:
            if "::" in s or s.isidentifier():
                return TuningSymbol(s).r_repr()
            return f'"{s}"'

        def _convert_list(lvalue: list) -> str:
            return f"c({', '.join(map(str, lvalue))})"

        # Type converters
        # ToDo: Merge with conversions.base types
        type_converters = {
            TuningExpression: lambda x: x.r_repr(),
            dict: _convert_dict,
            str: _convert_string,
            list: _convert_list,
            tuple: _convert_list,
            bool: lambda x: "TRUE" if x else "FALSE",
            type(None): lambda _: "NULL",
        }

        converter = type_converters.get(type(arg))
        if converter is not None:
            return converter(arg)

        return str(arg)

    def r_repr(self) -> str:
        """Convert the function call to its R representation.

        Returns:
            str: The R code string representation of the function call.
        """
        args = [self._convert_arg(arg) for arg in self.args]
        args.extend(
            f"{key} = {self._convert_arg(val)}" for key, val in self.kwargs.items()
        )
        return f"{self.func}({', '.join(args)})"


def hparam(func_name: str, *args: Any, **kwargs: Any) -> TuningFunctionCall:
    """Create an R function call expression.

    This function creates an R function call expression that can be used to represent
    R function calls in Python code. The resulting expression can be converted to
    R code using the ``r_repr()`` method.

    Args:
        func_name: The name of the R function to call.

        *args: Positional arguments for the function call.

        **kwargs: Keyword arguments for the function call.

    Returns:
        RCall: An R function call expression.
    """
    return TuningFunctionCall(func_name, *args, **kwargs)
