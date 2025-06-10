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

"""pysits module."""

from .settings import __version__
from .sits.classification import sits_classify, sits_label_classification, sits_smooth
from .sits.colors import (
    sits_colors,
    sits_colors_reset,
    sits_colors_set,
    sits_colors_show,
)
from .sits.config import sits_config, sits_config_show, sits_config_user_file
from .sits.context import (
    cerrado_2classes,
    point_mt_6bands,
    samples_l8_rondonia_2bands,
    samples_modis_ndvi,
)
from .sits.cube import (
    sits_clean,
    sits_colors_qgis,
    sits_combine_predictions,
    sits_confidence_sampling,
    sits_cube,
    sits_cube_copy,
    sits_reclassify,
    sits_regularize,
    sits_uncertainty,
    sits_uncertainty_sampling,
    sits_variance,
)
from .sits.data import (
    sits_apply,
    sits_bands,
    sits_bbox,
    sits_labels,
    sits_labels_summary,
    sits_list_collections,
    sits_merge,
    sits_mixture_model,
    sits_reduce,
    sits_select,
    sits_timeline,
)
from .sits.data import sits_summary as summary
from .sits.exporters import sits_as_geopandas, sits_as_xarray, sits_to_csv, sits_to_xlsx
from .sits.impute import impute_linear, sits_impute
from .sits.ml import (
    sits_kfold_validate,
    sits_lighttae,
    sits_mlp,
    sits_rfor,
    sits_svm,
    sits_tae,
    sits_tempcnn,
    sits_train,
    sits_xgboost,
)
from .sits.segment import sits_segment, sits_slic
from .sits.tiles import sits_mgrs_to_roi, sits_tiles_to_roi
from .sits.ts import (
    sits_cluster_clean,
    sits_cluster_dendro,
    sits_cluster_frequency,
    sits_get_data,
    sits_patterns,
    sits_pred_features,
    sits_pred_normalize,
    sits_pred_references,
    sits_pred_sample,
    sits_predictors,
    sits_reduce_imbalance,
    sits_sample,
    sits_sampling_design,
    sits_sgolay,
    sits_show_prediction,
    sits_som_clean_samples,
    sits_som_evaluate_cluster,
    sits_som_map,
    sits_stats,
    sits_stratified_sampling,
    sits_whittaker,
)
from .sits.utils import (
    load_samples_dataset,
    r_package_dir,
    r_set_seed,
    read_rds,
)
from .sits.visualization import sits_plot as plot

__all__ = (
    # Classification
    "sits_classify",
    "sits_smooth",
    "sits_label_classification",
    # Cube
    "sits_cube",
    "sits_clean",
    "sits_combine_predictions",
    "sits_reclassify",
    "sits_regularize",
    "sits_cube_copy",
    "sits_colors_qgis",
    "sits_uncertainty",
    "sits_uncertainty_sampling",
    "sits_confidence_sampling",
    "sits_variance",
    # Colors
    "sits_colors",
    "sits_colors_reset",
    "sits_colors_set",
    "sits_colors_show",
    # Configuration
    "sits_config",
    "sits_config_show",
    "sits_config_user_file",
    # Data management
    "sits_bands",
    "sits_timeline",
    "sits_labels",
    "sits_list_collections",
    "sits_bbox",
    "sits_select",
    "sits_merge",
    "sits_mixture_model",
    "summary",
    "sits_labels_summary",
    "sits_cluster_dendro",
    "sits_cluster_frequency",
    "sits_cluster_clean",
    "sits_reduce",
    # Machine Learning methods
    "sits_train",
    "sits_mlp",
    "sits_rfor",
    "sits_tempcnn",
    "sits_lighttae",
    "sits_svm",
    "sits_xgboost",
    "sits_tae",
    "sits_kfold_validate",
    # Impute
    "sits_impute",
    "impute_linear",
    # Time-series
    "sits_show_prediction",
    "sits_sgolay",
    "sits_whittaker",
    "sits_get_data",
    "sits_stats",
    "sits_predictors",
    "sits_pred_features",
    "sits_pred_normalize",
    "sits_pred_references",
    "sits_pred_sample",
    "sits_som_map",
    "sits_som_evaluate_cluster",
    "sits_som_clean_samples",
    "sits_patterns",
    "sits_sample",
    "sits_reduce_imbalance",
    "sits_sampling_design",
    "sits_stratified_sampling",
    # Tiles
    "sits_mgrs_to_roi",
    "sits_tiles_to_roi",
    # Segments
    "sits_segment",
    "sits_slic",
    # Apply
    "sits_apply",
    # Exporters
    "sits_to_csv",
    "sits_as_xarray",
    "sits_as_geopandas",
    "sits_to_xlsx",
    # Visualization
    "plot",
    # Context data
    "samples_l8_rondonia_2bands",
    "samples_modis_ndvi",
    "point_mt_6bands",
    "cerrado_2classes",
    # Utils
    "read_rds",
    "r_package_dir",
    "r_set_seed",
    "load_samples_dataset",
    # Package settings
    "__version__",
)
