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

"""Tuning data models."""

from collections.abc import Callable
from typing import Any

from rpy2.rinterface_lib.sexp import NULLType
from rpy2.robjects.vectors import (
    BoolVector,
    FloatVector,
    IntVector,
    ListVector,
    StrVector,
)

from pysits.conversions.common import (
    R_DEPARSED_PREFIXES,
    convert_to_python,
    eval_r_deparsed,
    eval_r_language,
)
from pysits.models.data.base import SITSData
from pysits.models.data.matrix import SITSConfusionMatrix
from pysits.models.data.ts import SITSTimeSeriesModel

#
# Python types associated with each R vector type
#
HPARAM_TYPES = {
    BoolVector: "bool",
    IntVector: "int",
    FloatVector: "float",
    StrVector: "str",
}


#
# Tuning results columns that are not hyper-parameters
#
TUNING_METRICS = ("accuracy", "kappa", "acc", "samples_validation")


#
# Utilities
#
def convert_hparam(value: Any) -> Any:
    """Convert a hyper-parameter value from R to Python.

    Args:
        value: The hyper-parameter value to convert.

    Returns:
        Any: Converted Python object.
    """
    value = eval_r_deparsed(value)

    for vector_type, as_type in HPARAM_TYPES.items():
        if isinstance(value, vector_type):
            return convert_to_python(value, as_type=as_type)

    return convert_to_python(value)


#
# Classes
#
class SITSTuningResults(SITSData):
    """Base class for sits accuracy results."""

    #
    # Convertions
    #
    def _convert_from_r(self, instance: Any) -> Any:
        """Convert data from R to Python.

        Args:
            instance: The R instance to convert.

        Returns:
            The converted Python object.
        """
        return instance

    def _convert_attribute(self, attribute: str, transform_func: Callable) -> list[Any]:
        """Convert a list of data from R to Python.

        Args:
            attribute: The name of the attribute to convert.

            transform_func: Function to transform each element.

        Returns:
            List of converted Python objects, with NULL values converted to None.
        """
        values = self._instance.rx2(attribute)

        if isinstance(values, NULLType):
            return [None for i in range(len(self._instance.rx2("accuracy")))]

        # Check if value is a deparsed R expression (e.g., "c(128, 128, 128)")
        is_vector_as_string = any(
            isinstance(x, str) and x.startswith(R_DEPARSED_PREFIXES) for x in values
        )

        if is_vector_as_string:
            return [transform_func(eval_r_deparsed(x)) for x in values]

        if isinstance(values, ListVector):
            return [
                transform_func(x) if not isinstance(x, NULLType) else None
                for x in values
            ]

        # Assume values is a Vector
        return transform_func(values)

    def _convert_from_r_list(self, attribute: str, as_type: str) -> list[Any]:
        """Convert a list of data from R to Python.

        Args:
            attribute: The name of the attribute to convert.

            transform_func: Function to transform each element.

        Returns:
            List of converted Python objects, with NULL values converted to None.
        """
        return self._convert_attribute(
            attribute, lambda x: convert_to_python(x, as_type=as_type)
        )

    #
    # Properties
    #
    @property
    def accuracy(self) -> list[float]:
        """Get the accuracy values from the tuning results.

        Returns:
            A list of float values representing the accuracy metrics.
        """
        return convert_to_python(self._instance.rx2("accuracy"), as_type="float")

    @property
    def kappa(self) -> list[float]:
        """Get the kappa values from the tuning results.

        Returns:
            A list of float values representing the kappa statistics.
        """
        return convert_to_python(self._instance.rx2("kappa"), as_type="float")

    @property
    def acc(self) -> list[SITSConfusionMatrix]:
        """Get the confusion matrices from the tuning results.

        Returns:
            A list of SITSConfusionMatrix objects containing the confusion matrices.
        """
        return [SITSConfusionMatrix(x) for x in self._instance.rx2("acc")]

    @property
    def samples_validation(self) -> list[SITSTimeSeriesModel | None]:
        """Get the validation samples from the tuning results.

        Returns:
            A list of SITSTimeSeriesModel objects or None values for validation samples.
        """
        return [
            SITSTimeSeriesModel(x) if not isinstance(x, NULLType) else None
            for x in self._instance.rx2("samples_validation")
        ]

    @property
    def cnn_layers(self) -> list[list[float]]:
        """Get the CNN layer configurations from the tuning results.

        Returns:
            A list with the CNN layer configuration of each trial.
        """
        return self._convert_from_r_list("cnn_layers", "float")

    @property
    def cnn_kernels(self) -> list[list[float]]:
        """Get the CNN kernel configurations from the tuning results.

        Returns:
            A list with the CNN kernel configuration of each trial.
        """
        return self._convert_from_r_list("cnn_kernels", "float")

    @property
    def cnn_dropout_rates(self) -> list[list[float]]:
        """Get the CNN dropout rates from the tuning results.

        Returns:
            A list with the CNN dropout rates of each trial.
        """
        return self._convert_from_r_list("cnn_dropout_rates", "float")

    @property
    def dense_layer_nodes(self) -> list[list[float]]:
        """Get the dense layer node configurations from the tuning results.

        Returns:
            A list with the dense layer node configuration of each trial.
        """
        return self._convert_from_r_list("dense_layer_nodes", "float")

    @property
    def dense_layer_dropout_rate(self) -> list[list[float]]:
        """Get the dense layer dropout rates from the tuning results.

        Returns:
            A list with the dense layer dropout rates of each trial.
        """
        return self._convert_from_r_list("dense_layer_dropout_rate", "float")

    @property
    def epochs(self) -> list[float]:
        """Get the number of epochs from the tuning results.

        Returns:
            A list of float values representing the number of epochs.
        """
        return self._convert_from_r_list("epochs", "float")

    @property
    def batch_size(self) -> list[float]:
        """Get the batch sizes from the tuning results.

        Returns:
            A list of float values representing the batch sizes.
        """
        return self._convert_from_r_list("batch_size", "float")

    @property
    def validation_split(self) -> list[float]:
        """Get the validation split ratios from the tuning results.

        Returns:
            A list of float values representing the validation split ratios.
        """
        return self._convert_from_r_list("validation_split", "float")

    @property
    def optimizer(self) -> list[str]:
        """Get the optimizer configurations from the tuning results.

        Returns:
            A list of strings representing the optimizer configurations.
        """
        return [eval_r_language(x).rclass[0] for x in self._instance.rx2("optimizer")]

    @property
    def opt_hparams(self) -> list[dict[str, Any]]:
        """Get the optimizer hyperparameters from the tuning results.

        Returns:
            A list of dictionaries containing optimizer hyperparameters.
            Each dictionary maps parameter names to their values.
        """
        return self._convert_attribute(
            "opt_hparams",
            lambda x: {str(k): convert_hparam(v) for k, v in x.items()},
        )

    @property
    def lr_decay_epochs(self) -> list[list[float]]:
        """Get the learning rate decay epochs from the tuning results.

        Returns:
            A list with the learning rate decay epochs of each trial.
        """
        return self._convert_from_r_list("lr_decay_epochs", "float")

    @property
    def lr_decay_rate(self) -> list[list[float]]:
        """Get the learning rate decay rates from the tuning results.

        Returns:
            A list with the learning rate decay rates of each trial.
        """
        return self._convert_from_r_list("lr_decay_rate", "float")

    @property
    def patience(self) -> list[float]:
        """Get the patience values from the tuning results.

        Returns:
            A list of float values representing the patience values.
        """
        return self._convert_from_r_list("patience", "float")

    @property
    def min_delta(self) -> list[float]:
        """Get the minimum delta values from the tuning results.

        Returns:
            A list of float values representing the minimum delta values.
        """
        return self._convert_from_r_list("min_delta", "float")

    @property
    def verbose(self) -> list[bool]:
        """Get the verbose flags from the tuning results.

        Returns:
            A list of boolean values representing the verbose flags.
        """
        return self._convert_from_r_list("verbose", "bool")

    @property
    def hparams(self) -> dict[str, list[Any]]:
        """Get all the hyper-parameters tuned, one value per trial.

        Returns:
            A dictionary mapping each hyper-parameter name to its values.
        """
        return {
            name: getattr(self, name)
            for name in self._instance.names
            if name not in TUNING_METRICS
        }

    #
    # Dunder methods
    #
    def __getattr__(self, name: str) -> list[Any]:
        """Get a hyper-parameter with no property associated with it.

        Args:
            name: The name of the hyper-parameter to get.

        Returns:
            A list with the hyper-parameter values, one per trial.
        """
        if name.startswith("_") or name not in self._instance.names:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

        return self._convert_attribute(name, convert_hparam)

    def __str__(self):
        """String representation."""
        return str(self._instance)

    def __repr__(self):
        """Representation."""
        return str(self._instance)

    def _repr_html_(self) -> str:
        """Create an HTML representation of the tuning results."""
        from pysits.jinja import get_template

        # Render the template
        return get_template("tuning.html").render(tuning_obj=self)
