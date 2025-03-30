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

"""machine-learning operations."""

from pysits.backend.sits import r_sits
from pysits.models import SITSCubeModel
from pysits.toolbox.conversions.base import rpy2_fix_type


@rpy2_fix_type
def sits_classify(*args, **kwargs):
    """Classify data.

    This function classifies a set of time series or data cube given a trained model
    prediction model created by ``sits_train``.
    """
    data = r_sits.sits_classify(*args, **kwargs)

    return SITSCubeModel(data)


@rpy2_fix_type
def sits_smooth(*args, **kwargs):
    """Smooth classification data.

    Takes a set of classified raster layers with probabilities, whose metadata is
    created by ``sits_cube``, and applies a bayesian smoothing function.
    """
    data = r_sits.sits_smooth(*args, **kwargs)

    return SITSCubeModel(data)


@rpy2_fix_type
def sits_label_classification(*args, **kwargs):
    """Label probabilities data.

    Takes a set of classified raster layers with probabilities, and label them
    based on the maximum probability for each pixel.
    """
    data = r_sits.sits_label_classification(*args, **kwargs)

    return SITSCubeModel(data)
