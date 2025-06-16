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
from pysits.conversions.common import convert_to_python
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.accuracy import SITSConfusionMatrix
from pysits.models.data.base import SITStructureData
from pysits.models.data.frame import SITSFrame, SITSFrameNested, SITSFrameSF
from pysits.models.data.matrix import SITSMatrix
from pysits.models.data.table import SITSTable
from pysits.models.data.ts import SITSTimeSeriesModel, SITSTimeSeriesPatternsModel


#
# High-level operation
#
@function_call(r_pkg_sits.sits_get_data, SITSTimeSeriesModel)
@attach_doc("sits_get_data")
def sits_get_data(*args, **kwargs) -> SITSTimeSeriesModel:
    """Retrieve time series data from a data cube."""


@function_call(r_pkg_sits.sits_get_class, SITSFrame)
@attach_doc("sits_get_class")
def sits_get_class(*args, **kwargs) -> SITSFrame:
    """Get values from classified maps."""


@function_call(r_pkg_sits.sits_get_probs, lambda x: SITSFrameNested(x, ["neighbors"]))
@attach_doc("sits_get_probs")
def sits_get_probs(*args, **kwargs) -> SITSFrameNested:
    """Get probabilities from classified maps."""


@function_call(r_pkg_sits.sits_stats, SITStructureData)
@attach_doc("sits_stats")
def sits_stats(*args, **kwargs) -> SITStructureData:
    """Obtain statistics for all sample bands.

    ToDo:
        - Enhance result type to a Dict-like object.
    """


#
# Validation
#
@function_call(r_pkg_sits.sits_validate, SITSConfusionMatrix)
@attach_doc("sits_validate")
def sits_validate(*args, **kwargs) -> SITSConfusionMatrix:
    """Validate time series samples."""


#
# Predictors
#
@function_call(r_pkg_sits.sits_predictors, SITSFrame)
@attach_doc("sits_predictors")
def sits_predictors(*args, **kwargs) -> SITSFrame:
    """Obtain predictors for time series samples."""


@function_call(r_pkg_sits.sits_pred_features, SITSFrame)
@attach_doc("sits_pred_features")
def sits_pred_features(*args, **kwargs) -> SITSFrame:
    """Obtain numerical values of predictors for time series samples."""


@function_call(r_pkg_sits.sits_pred_normalize, SITSFrame)
@attach_doc("sits_pred_normalize")
def sits_pred_normalize(*args, **kwargs) -> SITSFrame:
    """Normalize predictor values."""


@function_call(
    r_pkg_sits.sits_pred_references, lambda x: convert_to_python(x, as_type="str")
)
@attach_doc("sits_pred_references")
def sits_pred_references(*args, **kwargs) -> list[str]:
    """Obtain categorical id and predictor labels for time series samples."""


@function_call(r_pkg_sits.sits_pred_sample, SITSFrame)
@attach_doc("sits_pred_sample")
def sits_pred_sample(*args, **kwargs) -> SITSFrame:
    """Obtain a fraction of the predictors data frame."""


@function_call(r_pkg_sits.sits_sample, SITSTimeSeriesModel)
@attach_doc("sits_sample")
def sits_sample(*args, **kwargs) -> SITSTimeSeriesModel:
    """Sample a percentage of a time series."""


@function_call(r_pkg_sits.sits_reduce_imbalance, SITSTimeSeriesModel)
@attach_doc("sits_reduce_imbalance")
def sits_reduce_imbalance(*args, **kwargs) -> SITSTimeSeriesModel:
    """Reduce imbalance in a set of samples."""


@function_call(r_pkg_sits.sits_show_prediction, SITSFrame)
@attach_doc("sits_show_prediction")
def sits_show_prediction(*args, **kwargs) -> SITSFrame:
    """Show prediction results."""


#
# Sampling
#
@function_call(r_pkg_sits.sits_sampling_design, SITSMatrix)
@attach_doc("sits_sampling_design")
def sits_sampling_design(*args, **kwargs) -> SITSMatrix:
    """Allocation of sample size to strata."""


@function_call(r_pkg_sits.sits_stratified_sampling, SITSFrameSF)
@attach_doc("sits_stratified_sampling")
def sits_stratified_sampling(*args, **kwargs) -> SITSFrameSF:
    """Allocation of sample size to strata."""


#
# SOM
#
@function_call(r_pkg_sits.sits_som_map, SITStructureData)
@attach_doc("sits_som_map")
def sits_som_map(*args, **kwargs) -> SITStructureData:
    """Build a SOM for quality analysis of time series samples."""


@function_call(r_pkg_sits.sits_som_evaluate_cluster, SITSFrame)
@attach_doc("sits_som_evaluate_cluster")
def sits_som_evaluate_cluster(*args, **kwargs) -> SITSFrame:
    """Evaluate cluster quality."""


@function_call(r_pkg_sits.sits_som_clean_samples, SITSTimeSeriesModel)
@attach_doc("sits_som_clean_samples")
def sits_som_clean_samples(*args, **kwargs) -> SITSTimeSeriesModel:
    """Cleans the samples based on SOM map information."""


#
# Dendrogram
#
@function_call(r_pkg_sits.sits_cluster_dendro, SITSTimeSeriesModel)
@attach_doc("sits_cluster_dendro")
def sits_cluster_dendro(*args, **kwargs) -> SITSTimeSeriesModel:
    """Find clusters in time series samples.

    ToDo:
        - ToDo: Add support for the `plot` argument.
    """


@function_call(r_pkg_sits.sits_cluster_frequency, SITSTable)
@attach_doc("sits_cluster_frequency")
def sits_cluster_frequency(*args, **kwargs) -> SITSTable:
    """Show label frequency in each cluster produced by dendrogram analysis."""


@function_call(r_pkg_sits.sits_cluster_clean, SITSTimeSeriesModel)
@attach_doc("sits_cluster_clean")
def sits_cluster_clean(*args, **kwargs) -> SITSTimeSeriesModel:
    """Removes labels that are minority in each cluster."""


#
# Patterns
#
@function_call(r_pkg_sits.sits_patterns, SITSTimeSeriesPatternsModel)
@attach_doc("sits_patterns")
def sits_patterns(*args, **kwargs) -> SITSTimeSeriesPatternsModel:
    """Find temporal patterns associated to a set of time series."""


#
# Filtering
#
@function_call(r_pkg_sits.sits_sgolay, SITSTimeSeriesModel)
@attach_doc("sits_sgolay")
def sits_sgolay(*args, **kwargs) -> SITSTimeSeriesModel:
    """Apply Savitzky-Golay filter to time series."""


@function_call(r_pkg_sits.sits_whittaker, SITSTimeSeriesModel)
@attach_doc("sits_whittaker")
def sits_whittaker(*args, **kwargs) -> SITSTimeSeriesModel:
    """Apply Whittaker filter to time series."""


#
# Distances
#
@function_call(r_pkg_sits.sits_geo_dist, SITSFrame)
@attach_doc("sits_geo_dist")
def sits_geo_dist(*args, **kwargs) -> SITSFrame:
    """Compute the minimum distances among samples and prediction points."""
