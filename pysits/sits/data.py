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

"""Data management operations."""

from datetime import date

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import function_call, r_to_python
from pysits.docs import attach_doc
from pysits.models import SITSFrame
from pysits.models.builder import data_class_selector


@function_call(r_pkg_sits.sits_bands, lambda x: r_to_python(x, as_type="str"))
@attach_doc("sits_bands")
def sits_bands(*args, **kwargs) -> list[str]:
    """Get datacube bands."""
    ...


@function_call(r_pkg_sits.sits_timeline, lambda x: r_to_python(x, as_type="date"))
@attach_doc("sits_timeline")
def sits_timeline(*args, **kwargs) -> list[date]:
    """Get datacube timeline."""
    ...


@function_call(r_pkg_sits.sits_labels, lambda x: r_to_python(x, as_type="str"))
@attach_doc("sits_labels")
def sits_labels(*args, **kwargs) -> list[str]:
    """Finds labels in a sits tibble or data cube."""
    ...


@function_call(r_pkg_sits.sits_bbox, SITSFrame)
@attach_doc("sits_bbox")
def sits_bbox(*args, **kwargs) -> SITSFrame:
    """Get bbox of sits tibble or data cube."""
    ...


@function_call(r_pkg_sits.sits_select, lambda x: data_class_selector(x)(x))
@attach_doc("sits_select")
def sits_select(*args, **kwargs) -> SITSFrame:
    """Select bands from a sits tibble or data cube."""
    ...


@function_call(r_pkg_sits.sits_merge, lambda x: data_class_selector(x)(x))
@attach_doc("sits_merge")
def sits_merge(*args, **kwargs) -> SITSFrame:
    """Merge two sits tibbles or data cubes."""
    ...


@function_call(r_pkg_sits.sits_list_collections, lambda x: None)
@attach_doc("sits_list_collections")
def sits_list_collections(*args, **kwargs) -> None:
    """List collections available."""
    ...
