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

"""Machine-learning operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import function_call
from pysits.conversions.clojure import closure_factory
from pysits.docs import attach_doc
from pysits.models import SITSMachineLearningMethod

#
# ML Methods
#
sits_rfor = closure_factory("sits_rfor")
sits_tae = closure_factory("sits_tae")
sits_tempcnn = closure_factory("sits_tempcnn")
sits_lighttae = closure_factory("sits_lighttae")
sits_mlp = closure_factory("sits_mlp")
sits_svm = closure_factory("sits_svm")
sits_xgboost = closure_factory("sits_xgboost")


#
# High-level utility operation
#
@function_call(r_pkg_sits.sits_train, SITSMachineLearningMethod)
@attach_doc("sits_train")
def sits_train(*args, **kwargs) -> SITSMachineLearningMethod:
    """Train a machine learning model."""
    ...
