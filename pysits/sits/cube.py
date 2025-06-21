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

import rpy2.robjects as ro

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import (
    function_call,
    rpy2_fix_type,
    rpy2_fix_type_custom,
)
from pysits.conversions.dsl.mask import MaskExpressionList
from pysits.docs import attach_doc
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.frame import SITSFrame


#
# Reclassify-specific converters functions
#
def convert_reclassify_rules(obj: object) -> MaskExpressionList:
    """Convert reclassify rules to a propert ExpressionList."""

    if not isinstance(obj, dict):
        raise ValueError("Reclassify rules must be a dictionary.")

    return MaskExpressionList(**obj)


#
# Reclassify-specific converters config
#
reclassify_converters = {
    "rules": convert_reclassify_rules,
}


#
# Cube
#
@function_call(r_pkg_sits.sits_cube, SITSCubeModel)
@attach_doc("sits_cube")
def sits_cube(*args, **kwargs) -> SITSCubeModel:
    """Create cubes."""


@function_call(r_pkg_sits.sits_regularize, SITSCubeModel)
@attach_doc("sits_regularize")
def sits_regularize(*args, **kwargs) -> SITSCubeModel:
    """Build a regular data cube from an irregular one."""


@function_call(r_pkg_sits.sits_cube_copy, SITSCubeModel)
@attach_doc("sits_cube_copy")
def sits_cube_copy(*args, **kwargs) -> SITSCubeModel:
    """Copy cubes."""


@function_call(r_pkg_sits.sits_mosaic, SITSCubeModel)
@attach_doc("sits_mosaic")
def sits_mosaic(*args, **kwargs) -> SITSCubeModel:
    """Mosaic classified cubes."""


#
# Probability and metrics
#
@function_call(r_pkg_sits.sits_variance, SITSCubeModel)
@attach_doc("sits_variance")
def sits_variance(*args, **kwargs) -> SITSCubeModel:
    """Calculate the variance of a probability cube."""


@function_call(r_pkg_sits.sits_uncertainty, SITSCubeModel)
@attach_doc("sits_uncertainty")
def sits_uncertainty(*args, **kwargs) -> SITSCubeModel:
    """Estimate classification uncertainty based on probs cube."""


@function_call(r_pkg_sits.sits_clean, SITSCubeModel)
@attach_doc("sits_clean")
def sits_clean(*args, **kwargs) -> SITSCubeModel:
    """Cleans a classified map using a local window."""


#
# Combine predictions
#
@function_call(r_pkg_sits.sits_combine_predictions, SITSCubeModel)
@attach_doc("sits_combine_predictions")
def sits_combine_predictions(*args, **kwargs) -> SITSCubeModel:
    """Estimate ensemble prediction based on list of probs cubes."""


#
# Sampling
#
@function_call(r_pkg_sits.sits_uncertainty_sampling, SITSFrame)
@attach_doc("sits_uncertainty_sampling")
def sits_uncertainty_sampling(*args, **kwargs) -> SITSFrame:
    """Suggest samples for enhancing classification accuracy."""


@function_call(r_pkg_sits.sits_confidence_sampling, SITSFrame)
@attach_doc("sits_confidence_sampling")
def sits_confidence_sampling(*args, **kwargs) -> SITSFrame:
    """Suggest high confidence samples to increase the training set."""


#
# Colors
#
@function_call(r_pkg_sits.sits_colors_qgis, lambda x: None)
@attach_doc("sits_colors_qgis")
def sits_colors_qgis(*args, **kwargs) -> None:
    """Function to save color table as QML style for data cube."""


#
# Base cube
#
@function_call(r_pkg_sits.sits_add_base_cube, SITSCubeModel)
@attach_doc("sits_add_base_cube")
def sits_add_base_cube(*args, **kwargs) -> SITSCubeModel:
    """Add base maps to a time series data cube."""


#
# Reclassify
#
@rpy2_fix_type_custom(converters=reclassify_converters)
@rpy2_fix_type
@attach_doc("sits_reclassify")
def sits_reclassify(
    cube: SITSCubeModel, mask: SITSCubeModel, rules: MaskExpressionList, *args, **kwargs
) -> SITSCubeModel:
    """Reclassify a classified cube."""
    params = []

    # Process parameters manually
    for k, v in kwargs.items():
        current_v = v[0]

        if k in ["output_dir", "version"]:
            current_v = f"'{current_v}'"

        elif k == "progress":
            current_v = "TRUE" if current_v else "FALSE"

        params.append(f"{k}={current_v}")

    # Build the ``sits_apply`` command manually to support
    # high-level expression definition (using string)
    command = f"""
        sits_reclassify(
            cube = {cube.r_repr()},
            mask = {mask.r_repr()},
            rules = {rules.r_repr()},
            {", ".join(params)}
        )
    """

    # Run operation
    result = ro.r(command)

    # Return
    return SITSCubeModel(result)


#
# Texture
#
@rpy2_fix_type
@attach_doc("sits_texture")
def sits_texture(cube, **kwargs) -> SITSCubeModel:
    """Apply a set of texture measures on a data cube."""
    params = []

    # Process parameters manually
    for k, v in kwargs.items():
        current_v = v[0]

        if k == "output_dir":
            current_v = f"'{current_v}'"

        elif k == "progress":
            current_v = "TRUE" if current_v else "FALSE"

        params.append(f"{k}={current_v}")

    # Build the ``sits_texture`` command manually to support
    # high-level expression definition (using string)
    command = f"""
        sits_texture(
            {cube.r_repr()},
            {", ".join(params)}
        )
    """

    # Run operation
    result = ro.r(command)

    # Return
    return SITSCubeModel(result)
