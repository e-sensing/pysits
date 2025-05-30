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

"""Time-series operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import function_call
from pysits.docs import attach_doc
from pysits.models import (
    SITSFrame,
    SITSTimeSeriesModel,
    SITStructureData,
)


#
# High-level operation
#
@function_call(r_pkg_sits.sits_get_data, SITSTimeSeriesModel)
@attach_doc("sits_get_data")
def sits_get_data(*args, **kwargs) -> SITSTimeSeriesModel:
    """Retrieve time series data from a data cube."""
    ...


@function_call(r_pkg_sits.sits_predictors, SITSFrame)
@attach_doc("sits_predictors")
def sits_predictors(*args, **kwargs) -> SITSFrame:
    """Obtain predictors for time series samples."""
    ...


#
# SOM
#
@function_call(r_pkg_sits.sits_som_map, SITStructureData)
@attach_doc("sits_som_map")
def sits_som_map(*args, **kwargs) -> SITStructureData:
    """Build a SOM for quality analysis of time series samples."""
    ...


@function_call(r_pkg_sits.sits_som_evaluate_cluster, SITSFrame)
@attach_doc("sits_som_evaluate_cluster")
def sits_som_evaluate_cluster(*args, **kwargs) -> SITSFrame:
    """Evaluate cluster quality."""
    ...


@function_call(r_pkg_sits.sits_som_clean_samples, SITSTimeSeriesModel)
@attach_doc("sits_som_clean_samples")
def sits_som_clean_samples(*args, **kwargs) -> SITSTimeSeriesModel:
    """Cleans the samples based on SOM map information."""
    ...


#
# Patterns
#
@function_call(r_pkg_sits.sits_patterns, SITSTimeSeriesModel)
@attach_doc("sits_patterns")
def sits_patterns(*args, **kwargs) -> SITSTimeSeriesModel:
    """Find temporal patterns associated to a set of time series."""
    ...


#
# Filtering
#
@function_call(r_pkg_sits.sits_sgolay, SITSTimeSeriesModel)
@attach_doc("sits_sgolay")
def sits_sgolay(*args, **kwargs) -> SITSTimeSeriesModel:
    """Apply Savitzky-Golay filter to time series."""
    ...


@function_call(r_pkg_sits.sits_whittaker, SITSTimeSeriesModel)
@attach_doc("sits_whittaker")
def sits_whittaker(*args, **kwargs) -> SITSTimeSeriesModel:
    """Apply Whittaker filter to time series."""
    ...
