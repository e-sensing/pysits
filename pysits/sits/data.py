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

import rpy2.robjects as ro
from rpy2.robjects import globalenv as rpy2_globalenv

from pysits.backend.functions import r_fnc_summary
from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.common import convert_to_python
from pysits.conversions.decorators import function_call, rpy2_fix_type
from pysits.docs import attach_doc
from pysits.models.data.base import SITSData
from pysits.models.data.frame import SITSFrame
from pysits.models.resolver import (
    resolve_and_invoke_accuracy_class,
    resolve_and_invoke_content_class,
)


@function_call(r_pkg_sits.sits_bands, lambda x: convert_to_python(x, as_type="str"))
@attach_doc("sits_bands")
def sits_bands(*args, **kwargs) -> list[str]:
    """Get datacube bands."""


@function_call(r_pkg_sits.sits_timeline, lambda x: convert_to_python(x, as_type="date"))
@attach_doc("sits_timeline")
def sits_timeline(*args, **kwargs) -> list[date]:
    """Get datacube timeline."""


@function_call(r_pkg_sits.sits_labels, lambda x: convert_to_python(x, as_type="str"))
@attach_doc("sits_labels")
def sits_labels(*args, **kwargs) -> list[str]:
    """Finds labels in a sits tibble or data cube."""


@function_call(r_pkg_sits.sits_bbox, SITSFrame)
@attach_doc("sits_bbox")
def sits_bbox(*args, **kwargs) -> SITSFrame:
    """Get bbox of sits tibble or data cube."""


@function_call(r_pkg_sits.sits_select, resolve_and_invoke_content_class)
@attach_doc("sits_select")
def sits_select(*args, **kwargs) -> SITSFrame:
    """Select bands from a sits tibble or data cube."""


@function_call(r_pkg_sits.sits_merge, resolve_and_invoke_content_class)
@attach_doc("sits_merge")
def sits_merge(*args, **kwargs) -> SITSFrame:
    """Merge two sits tibbles or data cubes."""


@function_call(r_pkg_sits.sits_mixture_model, resolve_and_invoke_content_class)
@attach_doc("sits_mixture_model")
def sits_mixture_model(*args, **kwargs) -> SITSFrame:
    """Multiple endmember spectral mixture analysis."""


@function_call(r_pkg_sits.sits_list_collections, lambda x: None)
@attach_doc("sits_list_collections")
def sits_list_collections(*args, **kwargs) -> None:
    """List collections available."""


@function_call(r_fnc_summary, resolve_and_invoke_content_class)
@attach_doc("summary")
def sits_summary(*args, **kwargs) -> str:
    """Summary of a sits data object."""


@function_call(r_pkg_sits.sits_labels_summary, resolve_and_invoke_content_class)
@attach_doc("sits_labels_summary")
def sits_labels_summary(*args, **kwargs) -> SITSFrame:
    """Inform label distribution of a set of time series.

    Notes:
        - Deprecated function. Use `summary` instead.
    """


@function_call(r_pkg_sits.sits_accuracy, resolve_and_invoke_accuracy_class)
@attach_doc("sits_accuracy")
def sits_accuracy(*args, **kwargs) -> SITSData:
    """Assess classification accuracy."""


@function_call(r_pkg_sits.sits_accuracy_summary, resolve_and_invoke_accuracy_class)
@attach_doc("sits_accuracy_summary")
def sits_accuracy_summary(*args, **kwargs) -> SITSData:
    """Print accuracy summary."""


#
# Apply operation
#
@rpy2_fix_type
@attach_doc("sits_apply")
def sits_apply(data, **kwargs) -> SITSFrame:
    """Apply a function on a set of time series."""
    params = []

    # Process parameters manually
    for k, v in kwargs.items():
        current_v = v[0]

        if k == "output_dir":
            current_v = f"'{current_v}'"

        elif k == "progress":
            current_v = "TRUE" if current_v else "FALSE"

        elif k == "normalized":
            current_v = "TRUE" if current_v else "FALSE"

        params.append(f"{k}={current_v}")

    # Build the ``sits_apply`` command manually to support
    # high-level expression definition (using string)
    command = f"""
        sits_apply(
            {data.r_repr()},
            {", ".join(params)}
        )
    """

    # Run operation
    result = ro.r(command)

    # Return
    return resolve_and_invoke_content_class(result)


#
# Reduce
#
@rpy2_fix_type
@attach_doc("sits_reduce")
def sits_reduce(data, impute_fn=None, **kwargs) -> SITSFrame:
    """Reduces a cube or samples from a summarization function."""
    params = []

    # Process impute function
    if impute_fn is not None:
        params.append(f"impute_fn = {impute_fn.r_repr()}")

    # Process remaining parameters
    for k, v in kwargs.items():
        current_v = v[0]

        if k == "output_dir":
            current_v = f"'{current_v}'"

        elif k == "progress":
            current_v = "TRUE" if current_v else "FALSE"

        params.append(f"{k}={current_v}")

    # Build the ``sits_reduce`` command manually to support
    # high-level expression definition (using string)
    command = f"""
        sits_reduce(
            data = {data.r_repr()},
            {", ".join(params)}
        )
    """

    # Run operation
    result = ro.r(command)

    # Check if the result is a time-series data frame. If so, convert reduced
    # date type to numeric.
    if "time_series" in result.colnames:
        # Define conversion function
        ro.r("""
            convert_ts_reduce <- 
            function(data, column_name = "time_series", exclude = "Index") {
                data |>
                    dplyr::mutate(
                        {{ column_name }} := purrr::map(
                            .data[[column_name]],
                            ~ {
                                .x |>
                                    dplyr::mutate(dplyr::across(
                                        .cols = !dplyr::all_of(exclude),
                                        .fns = ~ as.numeric(.)
                                    ))
                            }
                        )
                    )
            }
        """)

        convert_ts_reduce = rpy2_globalenv["convert_ts_reduce"]

        # Convert result
        result = convert_ts_reduce(result)

    # Return
    return resolve_and_invoke_content_class(result)
