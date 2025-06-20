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

"""DSL for mask operations."""

from typing import Any

from pysits.conversions.dsl.base import RExpression


#
# Base R expression class
#
class MaskExpression(RExpression):
    """Mask expression class."""

    #
    # Magic methods
    #
    def __eq__(self, other):
        return Eq(self, other)

    def __ne__(self, other):
        return Neq(self, other)

    def __lt__(self, other):
        return Lt(self, other)

    def __le__(self, other):
        return Le(self, other)

    def __gt__(self, other):
        return Gt(self, other)

    def __ge__(self, other):
        return Ge(self, other)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):  # for ~expr → maps to ``NOT``
        return Not(self)

    def __mod__(self, other: Any) -> None:
        """Disabled modulo operator to prevent confusion with R's %in% operator.

        Args:
            other: The right-hand operand (unused).

        Raises:
            NotImplementedError: Always raised to indicate that %in_ should
                                 be used instead.
        """
        raise NotImplementedError("Use %in_ for 'in' operation")

    #
    # Hashing
    #
    def __hash__(self) -> int:
        """Hash the expression."""
        return hash(self.r_repr())

    #
    # Abstract methods
    #
    def r_repr(self) -> str:
        """Convert the expression to its R string representation.

        Returns:
            str: The R code representation of the expression.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented
                                 by subclasses.
        """
        raise NotImplementedError()


#
# Helper function
#
def as_rexpr(x: int | float | str | MaskExpression) -> MaskExpression:
    """Convert a Python value to an R expression.

    Args:
        x: Value to convert, can be an integer, float, string or
            existing ``MaskExpression``.

    Returns:
        MaskExpression: The value wrapped in an appropriate
            ``MaskExpression`` subclass.

    Raises:
        TypeError: If the input type cannot be converted to an
            ``MaskExpression``s.
    """
    if isinstance(x, MaskExpression):
        return x

    elif isinstance(x, (int | float | str)):
        return Literal(x)

    raise TypeError(f"Cannot convert {type(x)} to MaskExpression")


#
# Variable (symbol)
#
class MaskVariable(MaskExpression):
    """Represents an R variable or symbol."""

    def __init__(self, name: str) -> None:
        self.name = name

    def r_repr(self) -> str:
        """Convert the variable to its R string representation.

        Returns:
            str: The variable name as it appears in R.
        """
        return self.name

    # Add mask %in_ [...] syntactic sugar
    def in_(self, values: list[int | float | str]) -> "In":
        """Create an R %in% operation.

        Args:
            values: List of values to check membership against.

        Returns:
            In: An expression representing `var %in% c(values)` in R.
        """
        return In(self, values)


#
# Literal value
#
class Literal(MaskExpression):
    """Represents a literal value in R code.

    Args:
        value (Union[int, float, str]): The Python value to be represented in R.
    """

    def __init__(self, value: int | float | str) -> None:
        self.value = value

    def r_repr(self) -> str:
        """Convert the literal to its R string representation.

        Returns:
            str: The R code representation of the literal value.
        """
        return repr(self.value)


#
# Binary operator
#
class BinaryOp(MaskExpression):
    """Base class for binary operators.

    Args:
        left (Union[MaskExpression, int, float, str]): Left operand.

        right (Union[MaskExpression, int, float, str]): Right operand.
    """

    op: str | None = None
    """Operator."""

    def __init__(
        self,
        left: MaskExpression | int | float | str,
        right: MaskExpression | int | float | str,
    ) -> None:
        self.left = as_rexpr(left)
        self.right = as_rexpr(right)

    def r_repr(self) -> str:
        """Convert the binary operation to its R string representation.

        Returns:
            str: The R code representation of the binary operation.
        """
        return f"({self.left.r_repr()} {self.op} {self.right.r_repr()})"


#
# Specific binary ops
#
class Eq(BinaryOp):
    """Represents equality comparison (==) in R."""

    op = "=="


class Neq(BinaryOp):
    """Represents inequality comparison (!=) in R."""

    op = "!="


class Lt(BinaryOp):
    """Represents less than comparison (<) in R."""

    op = "<"


class Le(BinaryOp):
    """Represents less than or equal comparison (<=) in R."""

    op = "<="


class Gt(BinaryOp):
    """Represents greater than comparison (>) in R."""

    op = ">"


class Ge(BinaryOp):
    """Represents greater than or equal comparison (>=) in R."""

    op = ">="


class And(BinaryOp):
    """Represents logical AND (&) in R."""

    op = "&"


class Or(BinaryOp):
    """Represents logical OR (|) in R."""

    op = "|"


#
# Unary operator (NOT)
#
class Not(MaskExpression):
    """Represents logical NOT (!) in R.

    Args:
        expr (Union[RExpr, int, float, str]): Expression to negate.
    """

    def __init__(self, expr: MaskExpression | int | float | str) -> None:
        self.expr = as_rexpr(expr)

    def r_repr(self) -> str:
        """Convert the NOT operation to its R string representation.

        Returns:
            str: The R code representation of the NOT operation.
        """
        return f"!({self.expr.r_repr()})"


#
# In operator: mask %in% c(...)
#
class In(MaskExpression):
    """Represents the %in% operator in R.

    Args:
        left (Union[RExpr, int, float, str]): Value to check.

        values (List[Union[int, float, str]]): List of values to check against.
    """

    def __init__(
        self, left: MaskExpression | int | float | str, values: list[int | float | str]
    ) -> None:
        self.left = as_rexpr(left)
        self.values = values

    def r_repr(self) -> str:
        """Convert the %in% operation to its R string representation.

        Returns:
            str: The R code representation of the %in% operation.
        """
        values_str = ", ".join(repr(v) for v in self.values)
        return f"{self.left.r_repr()} %in% c({values_str})"


#
# List of expressions
#
class MaskExpressionList(MaskExpression):
    """Represents a named list of R expressions.

    Args:
        **entries (Dict[str, RExpr]): Keyword arguments mapping names to expressions.
    """

    def __init__(self, **entries: dict[str, MaskExpression]) -> None:
        self.entries = entries

    def r_repr(self) -> str:
        """Convert the expression list to its R string representation.

        Returns:
            str: The R code representation of the named list.
        """
        entries_str = ",\n    ".join(
            f'"{key}" = {expr.r_repr()}' for key, expr in self.entries.items()
        )
        return f"list(\n    {entries_str}\n)"


#
# Mask variables
#
MaskValue = MaskVariable("mask")
"""Mask variable for reclassify operations."""
