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

from sitsflow.backend.sits import r_sits
from sitsflow.factory import factory_function
from sitsflow.models import SITSMachineLearningMethod
from sitsflow.types import rpy2_fix_type


#
# Random Forest
#
sits_rfor = factory_function("sits_rfor")


#
# TempCNN
#
sits_tempcnn = factory_function("sits_tempcnn")


#
# Light TAE
#
sits_lighttae = factory_function("sits_lighttae")


#
# Multi-layer perceptron
#
sits_mlp = factory_function("sits_mlp")


#
# High-level utility operation
#
@rpy2_fix_type
def sits_train(*args, **kwargs):
    instance = r_sits.sits_train(*args, **kwargs)

    return SITSMachineLearningMethod(instance)
