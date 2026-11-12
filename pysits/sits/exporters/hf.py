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

"""HuggingFace exporter."""

from pysits.backend.functions import r_fnc_unname
from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.common import convert_to_r
from pysits.conversions.decorators import function_call, rpy2_fix_type_custom
from pysits.docs import attach_doc
from pysits.models.data.base import SITStructureData
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.models.ml import SITSMachineLearningMethod
from pysits.models.resolver import resolve_and_invoke_content_class


#
# HuggingFace-specific converters functions
#
def convert_hf_cubes(obj: object) -> object:
    """Convert a list of cubes to an unnamed R list."""
    if isinstance(obj, list | tuple):
        return r_fnc_unname(convert_to_r(obj))

    return obj


#
# HuggingFace-specific converters config
#
hf_converters = {
    "cube": convert_hf_cubes,
}


#
# HuggingFace
#
@function_call(r_pkg_sits.sits_from_hf, resolve_and_invoke_content_class)
@attach_doc("sits_from_hf")
def sits_from_hf(
    *args, **kwargs
) -> SITSCubeModel | SITSTimeSeriesModel | SITSMachineLearningMethod:
    """Read data cubes, samples and models shared on HuggingFace."""


@rpy2_fix_type_custom(converters=hf_converters)
@function_call(r_pkg_sits.sits_to_hf, SITStructureData)
@attach_doc("sits_to_hf")
def sits_to_hf(
    cube: SITSCubeModel | list[SITSCubeModel], *args, **kwargs
) -> SITStructureData:
    """Describe a data cube as a HuggingFace dataset."""


@function_call(r_pkg_sits.sits_config_to_hf, SITStructureData)
@attach_doc("sits_config_to_hf")
def sits_config_to_hf(*args, **kwargs) -> SITStructureData:
    """Describe a collection of sits as a HuggingFace dataset."""
