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

import cloudpickle
import pytest

from pysits.models.ml import SITSMachineLearningMethod
from pysits.sits.classification import sits_classify
from pysits.sits.context import (
    point_mt_6bands,
    samples_l8_rondonia_2bands,
    samples_modis_ndvi,
)
from pysits.sits.data import sits_labels, sits_select
from pysits.sits.ml import (
    sits_formula_linear,
    sits_formula_logref,
    sits_lightgbm,
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
    sits_lightgbm,
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


@pytest.mark.parametrize("model_fn", ALL_MODELS)
def test_model_serialization(model_fn, tmp_path):
    """Test model serialization."""
    ml_method = model_fn()
    model = sits_train(samples_modis_ndvi, ml_method=ml_method)

    assert isinstance(model, SITSMachineLearningMethod)

    # Serialize model
    serialized_model = cloudpickle.dumps(model)

    # Save serialized model to file
    model_file = tmp_path / "model.pkl"

    with model_file.open("wb") as f:
        f.write(serialized_model)

    # Load serialized model from file
    with model_file.open("rb") as f:
        loaded_model = cloudpickle.load(f)

    assert isinstance(loaded_model, SITSMachineLearningMethod)

    # Classify a time-series point
    point_ndvi = sits_select(point_mt_6bands, bands=("NDVI"))
    point_class = sits_classify(data=point_ndvi, ml_model=loaded_model)

    assert point_class.shape[0] == 1  # noqa: PLR2004 - number of points
    assert len(sits_labels(point_class)) == 1  # noqa: PLR2004 - number of labels


def test_model_svm_params():
    """Test SVM parameters."""

    model_linear = sits_train(
        samples_l8_rondonia_2bands,
        ml_method=sits_svm(formula=sits_formula_linear()),
    )

    model_logref = sits_train(
        samples_l8_rondonia_2bands,
        ml_method=sits_svm(formula=sits_formula_logref()),
    )

    assert isinstance(model_linear, SITSMachineLearningMethod)
    assert isinstance(model_logref, SITSMachineLearningMethod)


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
