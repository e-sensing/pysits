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

"""sits tuning module."""

from collections.abc import Callable
from typing import Any

import rpy2.robjects as ro
from rpy2.robjects.vectors import ListVector

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call, rpy2_fix_type_custom
from pysits.conversions.dsl.tuning import TuningFunctionCall
from pysits.docs import attach_doc
from pysits.models.data.tuning import SITSTuningResults


#
# Tuning-specific converters functions
#
def convert_tuning_params(obj: TuningFunctionCall) -> ListVector:
    """Convert tuning params to a propert ListVector."""

    return ro.r(obj.r_repr())


def convert_ml_method(obj: Callable) -> Callable:
    """Convert ml_method to a propert SITSMachineLearningMethod."""

    return getattr(r_pkg_sits, obj.__name__)


#
# Tuning-specific converters config
#
tuning_converters = {
    "params": convert_tuning_params,
    "ml_method": convert_ml_method,
}


def sits_tuning_hparams(*args: Any, **kwargs: Any) -> TuningFunctionCall:
    """Create an R function call for ``sits_tuning_hparams``.

    This function creates an R function call expression for the ``sits_tuning_hparams``
    function, which is used to specify hyperparameters for ``sits_tuning``.

    Args:
        optimizer: The name of the optimizer to use (e.g., "torch::optim_adam").

        opt_hparams: A dictionary of hyperparameters for the optimizer.

        *args: Additional positional arguments for the function call.

        **kwargs: Additional keyword arguments for the function call.

    Returns:
        RCall: An R function call expression for sits_tuning_hparams.
    """
    return TuningFunctionCall("sits_tuning_hparams", *args, **kwargs)


@rpy2_fix_type_custom(converters=tuning_converters)
@function_call(r_pkg_sits.sits_tuning, SITSTuningResults)
@attach_doc("sits_tuning")
def sits_tuning(data, **kwargs) -> SITSTuningResults:
    """Tuning machine learning models hyper-parameters."""
