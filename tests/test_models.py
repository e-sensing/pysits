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

"""Unit tests for ml/dl models."""

import pytest

from pysits.models import SITSMachineLearningMethod
from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.ml import (
    sits_lighttae,
    sits_mlp,
    sits_model_export,
    sits_resnet,
    sits_rfor,
    sits_svm,
    sits_tae,
    sits_tempcnn,
    sits_train,
    sits_xgboost,
)

#
# Models available to test
#
ALL_MODELS = [
    sits_tae,
    sits_tempcnn,
    sits_lighttae,
    sits_mlp,
    sits_resnet,
    sits_rfor,
    sits_svm,
    sits_xgboost,
]


#
# Test training for all available models
#
@pytest.mark.parametrize("model_fn", ALL_MODELS)
def test_model_training(model_fn):
    """Test training for all available models."""
    try:
        # Create model instance with parameters
        ml_method = model_fn()

        # Train model
        model = sits_train(samples_l8_rondonia_2bands, ml_method=ml_method)

        # Basic assertions to verify the model was trained
        assert model is not None
        assert isinstance(model, SITSMachineLearningMethod)

    except Exception as e:
        pytest.fail(f"Training failed: {str(e)}")


#
# Test model export
#
def test_model_export():
    """Test model export."""
    # Train model
    model = sits_train(samples_l8_rondonia_2bands, ml_method=sits_svm())

    # Try to export model
    with pytest.raises(NotImplementedError):
        sits_model_export(model)
