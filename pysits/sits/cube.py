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

"""Cube operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import function_call
from pysits.docs import attach_doc
from pysits.models import SITSCubeModel, SITSFrame


#
# High-level operations
#
@function_call(r_pkg_sits.sits_cube, SITSCubeModel)
@attach_doc("sits_cube")
def sits_cube(*args, **kwargs) -> SITSCubeModel:
    """Create cubes."""
    ...


@function_call(r_pkg_sits.sits_regularize, SITSCubeModel)
@attach_doc("sits_regularize")
def sits_regularize(*args, **kwargs) -> SITSCubeModel:
    """Build a regular data cube from an irregular one."""
    ...


@function_call(r_pkg_sits.sits_variance, SITSCubeModel)
@attach_doc("sits_variance")
def sits_variance(*args, **kwargs) -> SITSCubeModel:
    """Calculate the variance of a probability cube."""
    ...


@function_call(r_pkg_sits.sits_cube_copy, SITSCubeModel)
@attach_doc("sits_cube_copy")
def sits_cube_copy(*args, **kwargs) -> SITSCubeModel:
    """Copy cubes."""
    ...


@function_call(r_pkg_sits.sits_uncertainty, SITSCubeModel)
@attach_doc("sits_uncertainty")
def sits_uncertainty(*args, **kwargs) -> SITSCubeModel:
    """Estimate classification uncertainty based on probs cube."""
    ...


@function_call(r_pkg_sits.sits_clean, SITSCubeModel)
@attach_doc("sits_clean")
def sits_clean(*args, **kwargs) -> SITSCubeModel:
    """Cleans a classified map using a local window."""
    ...


@function_call(r_pkg_sits.sits_combine_predictions, SITSCubeModel)
@attach_doc("sits_combine_predictions")
def sits_combine_predictions(*args, **kwargs) -> SITSCubeModel:
    """Estimate ensemble prediction based on list of probs cubes."""
    ...


@function_call(r_pkg_sits.sits_uncertainty_sampling, SITSFrame)
@attach_doc("sits_uncertainty_sampling")
def sits_uncertainty_sampling(*args, **kwargs) -> SITSCubeModel:
    """Suggest samples for enhancing classification accuracy."""
    ...


@function_call(r_pkg_sits.sits_colors_qgis, lambda x: None)
@attach_doc("sits_colors_qgis")
def sits_colors_qgis(*args, **kwargs) -> None:
    """Function to save color table as QML style for data cube."""
    ...
