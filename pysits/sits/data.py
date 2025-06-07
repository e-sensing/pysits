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

from pysits.backend.functions import r_fnc_summary
from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import convert_to_python
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models import SITSFrame
from pysits.models.builder import resolve_and_invoke_data_class


@function_call(r_pkg_sits.sits_bands, lambda x: convert_to_python(x, as_type="str"))
@attach_doc("sits_bands")
def sits_bands(*args, **kwargs) -> list[str]:
    """Get datacube bands."""
    ...


@function_call(r_pkg_sits.sits_timeline, lambda x: convert_to_python(x, as_type="date"))
@attach_doc("sits_timeline")
def sits_timeline(*args, **kwargs) -> list[date]:
    """Get datacube timeline."""
    ...


@function_call(r_pkg_sits.sits_labels, lambda x: convert_to_python(x, as_type="str"))
@attach_doc("sits_labels")
def sits_labels(*args, **kwargs) -> list[str]:
    """Finds labels in a sits tibble or data cube."""
    ...


@function_call(r_pkg_sits.sits_bbox, SITSFrame)
@attach_doc("sits_bbox")
def sits_bbox(*args, **kwargs) -> SITSFrame:
    """Get bbox of sits tibble or data cube."""
    ...


@function_call(r_pkg_sits.sits_select, resolve_and_invoke_data_class)
@attach_doc("sits_select")
def sits_select(*args, **kwargs) -> SITSFrame:
    """Select bands from a sits tibble or data cube."""
    ...


@function_call(r_pkg_sits.sits_merge, resolve_and_invoke_data_class)
@attach_doc("sits_merge")
def sits_merge(*args, **kwargs) -> SITSFrame:
    """Merge two sits tibbles or data cubes."""
    ...


@function_call(r_pkg_sits.sits_mixture_model, resolve_and_invoke_data_class)
@attach_doc("sits_mixture_model")
def sits_mixture_model(*args, **kwargs) -> SITSFrame:
    """Multiple endmember spectral mixture analysis."""
    ...


@function_call(r_pkg_sits.sits_list_collections, lambda x: None)
@attach_doc("sits_list_collections")
def sits_list_collections(*args, **kwargs) -> None:
    """List collections available."""
    ...


@function_call(r_fnc_summary, resolve_and_invoke_data_class)
@attach_doc("summary")
def sits_summary(*args, **kwargs) -> str:
    """Summary of a sits data object."""
    ...


@function_call(r_pkg_sits.sits_labels_summary, resolve_and_invoke_data_class)
@attach_doc("sits_labels_summary")
def sits_labels_summary(*args, **kwargs) -> SITSFrame:
    """Inform label distribution of a set of time series.

    Notes:
        - Deprecated function. Use `summary` instead.
    """
    ...
