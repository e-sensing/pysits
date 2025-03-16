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

"""segment operations."""

from sitsflow import types as type_utils
from sitsflow.backend.sits import r_sits
from sitsflow.factory import factory_function
from sitsflow.models import SITSCubeModel

#
# Segmentation functions
#
sits_slic = factory_function("sits_slic")


#
# Segmentation operation
#
@type_utils.rpy2_fix_type
def sits_segment(*args, **kwargs):
    """Segment an image.

    Apply a spatial-temporal segmentation on a data cube based on a
    user defined segmentation function.
    """
    cube = r_sits.sits_segment(*args, **kwargs)
    return SITSCubeModel(cube)
