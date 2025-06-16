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

"""Unit tests for DSL operations."""

from pysits.conversions.dsl.mask import MaskExpressionList, MaskVariable


def test_expression_list_conversion():
    """Test conversion of expression list to R representation."""
    # Create a variable for the mask
    mask = MaskVariable("mask")

    # Create the expression list with a reduced set of samples
    expr_list = MaskExpressionList(
        **dict(
            Water_Mask=(mask == "Water"),
            NonForest_Mask=mask.in_(["NonForest", "NonForest2"]),
        )
    )

    # Expected R representation
    expected = (
        "list(\n"
        "    \"Water_Mask\" = (mask == 'Water'),\n"
        "    \"NonForest_Mask\" = mask %in% c('NonForest', 'NonForest2')\n"
        ")"
    )

    # Test the conversion
    assert expr_list.r_repr() == expected


def test_variable_creation():
    """Test creation of variable."""
    var = MaskVariable("test_var")
    assert var.r_repr() == "test_var"


def test_equality_operation():
    """Test equality operation."""
    var = MaskVariable("test_var")
    eq_expr = var == "value"
    assert eq_expr.r_repr() == "(test_var == 'value')"


def test_in_operation():
    """Test in operation."""
    var = MaskVariable("test_var")
    in_expr = var.in_(["a", "b", "c"])
    assert in_expr.r_repr() == "test_var %in% c('a', 'b', 'c')"


def test_logical_operations():
    """Test logical operations."""
    var = MaskVariable("test_var")

    # Test AND
    and_expr = (var == "a") & (var == "b")
    assert and_expr.r_repr() == "((test_var == 'a') & (test_var == 'b'))"

    # Test OR
    or_expr = (var == "a") | (var == "b")
    assert or_expr.r_repr() == "((test_var == 'a') | (test_var == 'b'))"

    # Test NOT
    not_expr = ~(var == "a")
    assert not_expr.r_repr() == "!((test_var == 'a'))"
