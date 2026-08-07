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

"""Pandas extension models."""

from pandas import DataFrame as PandasDataFrame


class NestedFrame(PandasDataFrame):
    """A lightweight DataFrame subclass for nested column cells.

    All pandas operations work natively. Overrides ``__repr__`` to show
    a compact summary instead of the full table.
    """

    @property
    def _constructor(self):
        return NestedFrame

    def __repr__(self):
        """Compact representation."""
        nrows, ncols = self.shape
        return f"NestedFrame({nrows} x {ncols})"
