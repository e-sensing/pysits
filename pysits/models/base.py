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

"""base models."""

import abc


class SITSBase(abc.ABC):
    """Base class for SITS models."""

    _instance = None
    """R Object instance."""

    #
    # Dunder methods (magic methods)
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        self._instance = instance
