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

"""Base data models."""

from pysits.models.base import SITSBase


class SITSData(SITSBase):
    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        # Convert data
        instance = self._convert_from_r(instance)

        # Initialize super class
        super().__init__(instance=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance, **kwargs):
        """Convert data from R to Python."""
        return None


class SITStructureData(SITSData):
    """Base class for sits structure (e.g., list) results."""

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert data from R to Python."""
        return instance
