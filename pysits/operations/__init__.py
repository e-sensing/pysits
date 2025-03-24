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

"""operations module."""

from .apply import sits_apply
from .classification import sits_classify, sits_label_classification, sits_smooth
from .cube import sits_cube, sits_regularize, sits_cube_copy
from .data import sits_bands, sits_timeline, sits_labels, sits_list_collections
from .ml import (
    sits_lighttae,
    sits_mlp,
    sits_rfor,
    sits_svm,
    sits_tae,
    sits_tempcnn,
    sits_train,
    sits_xgboost,
)
from .segment import sits_segment, sits_slic
from .ts import sits_get_data

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
    # Segments
    "sits_segment",
    "sits_slic",
    # Apply
    "sits_apply",
)
