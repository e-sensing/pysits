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

"""Color operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call, rpy2_fix_type
from pysits.docs import attach_doc
from pysits.models.data.frame import SITSFrame
from pysits.sits.visualization import sits_plot


@function_call(r_pkg_sits.sits_colors, SITSFrame)
@attach_doc("sits_colors")
def sits_colors(*args, **kwargs) -> SITSFrame:
    """List all supported legend colors."""


@function_call(r_pkg_sits.sits_colors_reset, lambda x: None)
@attach_doc("sits_colors_reset")
def sits_colors_reset(*args, **kwargs) -> None:
    """Reset color table."""


@function_call(r_pkg_sits.sits_colors_set, SITSFrame)
@attach_doc("sits_colors_set")
def sits_colors_set(*args, **kwargs) -> SITSFrame:
    """Set color table."""


@rpy2_fix_type
@attach_doc("sits_colors_show")
def sits_colors_show(*args, **kwargs) -> None:
    """Plot color table."""
    result = r_pkg_sits.sits_colors_show(*args, **kwargs)
    sits_plot(result)
