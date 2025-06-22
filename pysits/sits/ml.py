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

from typing import Any

from pysits.backend.loaders import load_function_from_package
from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.clojure import closure_factory
from pysits.conversions.common import convert_dict_like_as_list_to_r
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.ml import SITSMachineLearningMethod
from pysits.models.resolver import resolve_and_invoke_accuracy_class


#
# DL-specific converters functions
#
def convert_optimizer(obj: Any) -> Any:
    """Convert optimizer."""

    if isinstance(obj, str):
        return load_function_from_package(obj)

    raise ValueError(
        "Invalid optimizer format. Expected a string in the format 'package::function'."
    )


def convert_opt_hparams(obj: Any) -> Any:
    """Convert optimizer hyperparameters."""

    return convert_dict_like_as_list_to_r(obj)


#
# DL-specific converters config
#
dl_converters = {
    "optimizer": convert_optimizer,
    "opt_hparams": convert_opt_hparams,
}

#
# DL Methods
#
sits_tae = closure_factory("sits_tae", converters=dl_converters)
sits_tempcnn = closure_factory("sits_tempcnn", converters=dl_converters)
sits_lighttae = closure_factory("sits_lighttae", converters=dl_converters)
sits_mlp = closure_factory("sits_mlp", converters=dl_converters)
sits_resnet = closure_factory("sits_resnet", converters=dl_converters)


#
# ML Methods
#
sits_rfor = closure_factory("sits_rfor")
sits_svm = closure_factory("sits_svm")
sits_xgboost = closure_factory("sits_xgboost")
sits_lightgbm = closure_factory("sits_lightgbm")


#
# Extra parameters - SVM
#
sits_formula_logref = closure_factory("sits_formula_logref")
sits_formula_linear = closure_factory("sits_formula_linear")


#
# High-level utility operations
#
@function_call(r_pkg_sits.sits_train, SITSMachineLearningMethod)
@attach_doc("sits_train")
def sits_train(*args, **kwargs) -> SITSMachineLearningMethod:
    """Train a machine learning model."""


@function_call(r_pkg_sits.sits_kfold_validate, resolve_and_invoke_accuracy_class)
@attach_doc("sits_kfold_validate")
def sits_kfold_validate(*args, **kwargs) -> resolve_and_invoke_accuracy_class:
    """Cross-validate time series samples."""


#
# Model export functions
#
def sits_model_export(*args, **kwargs) -> None:
    """Export a machine learning model.

    This function is only available in R.

    Raises:
        NotImplementedError: Function is only available in R.
    """
    raise NotImplementedError("``sits_model_export`` is only available in R")
