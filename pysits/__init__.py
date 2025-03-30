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

from .sits.apply import sits_apply
from .sits.classification import sits_classify, sits_label_classification, sits_smooth
from .sits.cube import sits_cube, sits_cube_copy, sits_regularize
from .sits.data import sits_bands, sits_labels, sits_list_collections, sits_timeline
from .sits.exporters import sits_as_xarray
from .sits.ml import (
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
from .sits.ts import sits_get_data, sits_predictors
from .sits.utils import read_sits_rds
from .sits.visualization import sits_plot as plot

__all__ = (
    # Classification
    "sits_classify",
    "sits_smooth",
    "sits_label_classification",
    # Cube
    "sits_cube",
    "sits_regularize",
    "sits_cube_copy",
    # Data management
    "sits_bands",
    "sits_timeline",
    "sits_labels",
    "sits_list_collections",
    # Machine Learning methods
    "sits_train",
    "sits_mlp",
    "sits_rfor",
    "sits_tempcnn",
    "sits_lighttae",
    "sits_svm",
    "sits_xgboost",
    "sits_tae",
    # Time series
    "sits_get_data",
    "sits_predictors",
    # Segments
    "sits_segment",
    "sits_slic",
    # Apply
    "sits_apply",
    # Exporters
    "sits_as_xarray",
    # Visualization
    "plot",
    # Utils
    "read_sits_rds",
)
