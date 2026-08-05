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

"""Unit tests for tuning operations."""

import pytest

from pysits.conversions.dsl.tuning import hparam
from pysits.models.data.tuning import SITSTuningResults
from pysits.sits.context import samples_modis_ndvi
from pysits.sits.ml import sits_tempcnn
from pysits.sits.tuning import sits_tuning, sits_tuning_hparams

#
# Hyper-parameters options available for tuning
#
CNN_LAYERS = [[128.0, 128.0, 128.0], [64.0, 64.0, 64.0]]
CNN_KERNELS = [[3.0, 3.0, 3.0], [5.0, 5.0, 5.0]]
BETAS = [[0.9, 0.999], [0.85, 0.99]]
OPTIMIZERS = ["optim_adamw", "optim_adam"]

#
# Number of trials used in the tests
#
TRIALS = 2


@pytest.fixture(scope="module")
def tuned_tempcnn() -> SITSTuningResults:
    """Tuning results of a ``sits_tempcnn`` model."""
    return sits_tuning(
        samples=samples_modis_ndvi,
        ml_method=sits_tempcnn,
        params=sits_tuning_hparams(
            cnn_layers=hparam("choice", *[tuple(x) for x in CNN_LAYERS]),
            cnn_kernels=hparam("choice", *[tuple(x) for x in CNN_KERNELS]),
            epochs=1,
            optimizer=hparam("choice", *[f"torch::{x}" for x in OPTIMIZERS]),
            opt_hparams=dict(
                lr=hparam("loguniform", 10**-2, 10**-4),
                betas=hparam("choice", *[tuple(x) for x in BETAS]),
            ),
        ),
        trials=TRIALS,
        multicores=1,
    )


def test_tuning_metrics(tuned_tempcnn):
    """Test tuning metrics results."""
    assert isinstance(tuned_tempcnn, SITSTuningResults)

    assert len(tuned_tempcnn.accuracy) == TRIALS
    assert len(tuned_tempcnn.kappa) == TRIALS
    assert len(tuned_tempcnn.acc) == TRIALS


def test_tuning_vector_hparams(tuned_tempcnn):
    """Test tuning results of hyper-parameters defined as vectors."""
    assert len(tuned_tempcnn.cnn_layers) == TRIALS
    assert len(tuned_tempcnn.cnn_kernels) == TRIALS

    for layers, kernels in zip(tuned_tempcnn.cnn_layers, tuned_tempcnn.cnn_kernels):
        assert layers in CNN_LAYERS
        assert kernels in CNN_KERNELS


def test_tuning_scalar_hparams(tuned_tempcnn):
    """Test tuning results of hyper-parameters defined as scalars."""
    assert tuned_tempcnn.epochs == [[1.0]] * TRIALS
    assert tuned_tempcnn.validation_split == [[0.2]] * TRIALS
    assert tuned_tempcnn.verbose == [[False]] * TRIALS


def test_tuning_optimizer_hparams(tuned_tempcnn):
    """Test tuning results of optimizer hyper-parameters."""
    assert len(tuned_tempcnn.optimizer) == TRIALS

    for optimizer in tuned_tempcnn.optimizer:
        assert optimizer in OPTIMIZERS

    for opt_hparams in tuned_tempcnn.opt_hparams:
        assert len(opt_hparams["lr"]) == 1
        assert opt_hparams["betas"] in BETAS


def test_tuning_html_representation(tuned_tempcnn):
    """Test tuning HTML representation."""
    html = tuned_tempcnn._repr_html_()

    for layers in tuned_tempcnn.cnn_layers:
        assert str(layers) in html
