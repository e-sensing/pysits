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

"""Exporters module."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.frame import SITSFrame
from pysits.models.resolver import resolve_and_invoke_content_class


@function_call(r_pkg_sits.sits_as_sf, resolve_and_invoke_content_class)
@attach_doc("sits_as_geopandas")
def sits_as_geopandas(data: SITSFrame) -> SITSFrame:
    """Export a sits data object as an geopandas object."""
