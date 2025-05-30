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

"""Cube operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import function_call
from pysits.docs import attach_doc
from pysits.models import SITSCubeModel


#
# High-level operations
#
@function_call(r_pkg_sits.sits_cube, SITSCubeModel)
@attach_doc("sits_cube")
def sits_cube(*args, **kwargs) -> SITSCubeModel:
    """Create cubes."""
    ...


@function_call(r_pkg_sits.sits_regularize, SITSCubeModel)
@attach_doc("sits_regularize")
def sits_regularize(*args, **kwargs) -> SITSCubeModel:
    """Build a regular data cube from an irregular one."""
    ...


@function_call(r_pkg_sits.sits_cube_copy, SITSCubeModel)
@attach_doc("sits_cube_copy")
def sits_cube_copy(*args, **kwargs) -> SITSCubeModel:
    """Copy cubes."""
    ...
