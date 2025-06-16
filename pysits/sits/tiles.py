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

"""Tile-related operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.vector import SITSNamedVector


@function_call(r_pkg_sits.sits_mgrs_to_roi, SITSNamedVector)
@attach_doc("sits_mgrs_to_roi")
def sits_mgrs_to_roi(*args, **kwargs) -> SITSNamedVector:
    """Convert MGRS to ROI."""


@function_call(r_pkg_sits.sits_tiles_to_roi, SITSNamedVector)
@attach_doc("sits_tiles_to_roi")
def sits_tiles_to_roi(*args, **kwargs) -> SITSNamedVector:
    """Convert tiles to ROI."""
