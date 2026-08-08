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

"""Unit tests for representation learning models."""

import pytest
from conftest import r_class, r_closure_value, r_identical, r_opt_hparams

from pysits.models.ml import SITSRepresentationLearningMethod
from pysits.sits.context import samples_modis_ndvi
from pysits.sits.ml import (
    sits_barlow_twins,
    sits_contrastive_learning,
    sits_lighttae,
    sits_pre_train,
    sits_ssl_lejepa,
    sits_ssl_mae,
    sits_ssl_vicreg,
)

#
# Encoder methods available to test
#
ALL_ENCODER_METHODS = [
    sits_ssl_mae,
    sits_ssl_lejepa,
    sits_ssl_vicreg,
    sits_contrastive_learning,
    sits_barlow_twins,
]


#
# Test pre-training for all available encoder methods
#
@pytest.mark.parametrize("model_fn", ALL_ENCODER_METHODS)
def test_model_pre_training(model_fn):
    """Test pre-training for all available encoder methods."""
    try:
        # Create encoder method
        rl_method = model_fn(epochs=1)

        # Pre-train model
        model = sits_pre_train(
            samples=samples_modis_ndvi,
            rl_method=rl_method,
        )

        # Test!
        assert model is not None
        assert isinstance(model, SITSRepresentationLearningMethod)

    except Exception as e:
        pytest.fail(f"Pre-training failed: {str(e)}")


@pytest.mark.parametrize("model_fn", ALL_ENCODER_METHODS)
def test_model_pre_training_with_encoder_model(model_fn):
    """Test pre-training with a user-defined encoder model."""
    model = sits_pre_train(
        samples=samples_modis_ndvi,
        rl_method=model_fn(
            encoder_model=sits_lighttae(),
            epochs=1,
        ),
    )

    assert isinstance(model, SITSRepresentationLearningMethod)

    # The model was pre-trained with the encoder defined by the user
    # (`model_ltae`), and not with the default one (`model_tcnn`)
    assert "model_ltae" in r_class(r_closure_value(model._instance, "encoder"))


#
# Test encoder methods parameters
#
@pytest.mark.parametrize("model_fn", ALL_ENCODER_METHODS)
def test_encoder_method_encoder_model(model_fn):
    """Test encoder model defined by the user is used as is."""
    encoder_model = sits_lighttae(opt_hparams={"lr": 0.02})
    rl_method = model_fn(encoder_model=encoder_model)

    # The encoder model is passed to R untouched
    assert r_identical(r_closure_value(rl_method, "encoder_model"), encoder_model)

    # Including its own converted parameters
    assert r_opt_hparams(encoder_model) == {"lr": 0.02}


@pytest.mark.parametrize("model_fn", ALL_ENCODER_METHODS)
def test_encoder_method_converters(model_fn):
    """Test conversion of dl-specific parameters."""
    rl_method = model_fn(
        optimizer="torch::optim_adam",
        opt_hparams={"lr": 0.01, "eps": 1e-07},
    )

    # The optimizer is loaded from R (`optim_adam` is not the default optimizer)
    assert "optim_adam" in r_class(r_closure_value(rl_method, "optimizer"))

    # The hyperparameters are converted to an R list
    assert r_opt_hparams(rl_method) == {"lr": 0.01, "eps": 1e-07}
