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

"""Base DSL classes."""


class DSLObject:
    """Base class for DSL classes."""


class RExpression(DSLObject):
    def r_repr(self) -> str:
        """Convert the expression to its R representation.

        Returns:
            str: The R code string representation of the expression.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """String representation of the R expression.

        Returns:
            str: The R code string representation.
        """
        return self.r_repr()
