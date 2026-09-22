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

"""Files exporter."""

from pathlib import Path

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.frame import SITSFrame
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.models.resolver import resolve_and_invoke_content_class
from pysits.network import fetch_to_tempfile, is_remote


@function_call(r_pkg_sits.sits_to_csv, SITSFrame)
@attach_doc("sits_to_csv")
def sits_to_csv(*args, **kwargs) -> SITSFrame:
    """Export sits data as csv."""
    ...


@function_call(r_pkg_sits.sits_to_xlsx, lambda x: None)
@attach_doc("sits_to_xlsx")
def sits_to_xlsx(*args, **kwargs) -> None:
    """Save accuracy assessments as Excel files."""
    ...


@function_call(r_pkg_sits.sits_timeseries_to_csv, lambda x: None)
@attach_doc("sits_timeseries_to_csv")
def sits_timeseries_to_csv(*args, **kwargs) -> None:
    """Export a full sits timeseries to CSV format."""


@function_call(r_pkg_sits.sits_to_parquet, lambda x: None)
@attach_doc("sits_to_parquet")
def sits_to_parquet(*args, **kwargs) -> None:
    """Export sits time series to the Parquet format."""


@function_call(r_pkg_sits.sits_from_parquet, resolve_and_invoke_content_class)
def _sits_from_parquet(*args, **kwargs) -> SITSTimeSeriesModel:
    """Read sits time series from a local Parquet file."""


@attach_doc("sits_from_parquet")
def sits_from_parquet(file: str | Path) -> SITSTimeSeriesModel:
    """Read sits time series from the Parquet format."""
    # If file is remote
    if is_remote(file):
        # Download it to a temporary file
        with fetch_to_tempfile(str(file), suffix=".parquet") as local_file:
            # Read it
            return _sits_from_parquet(local_file)

    # Otherwise, read it directly
    return _sits_from_parquet(file)
