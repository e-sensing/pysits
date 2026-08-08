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

"""end-to-end embeddings test."""

from pathlib import Path

import pytest
from rpy2.rinterface_lib.embedded import RRuntimeError

from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.sits.context import samples_modis_ndvi
from pysits.sits.data import (
    sits_bands,
    sits_classify,
    sits_encode,
    sits_label_classification,
    sits_labels,
    sits_select,
    sits_timeline,
)
from pysits.sits.ml import (
    sits_barlow_twins,
    sits_contrastive_learning,
    sits_pre_train,
    sits_rfor,
    sits_ssl_lejepa,
    sits_ssl_mae,
    sits_ssl_vicreg,
    sits_train,
)
from pysits.sits.visualization import sits_plot

#
# Encoder configuration
#
EMBEDDING_DIM = 8
EMBEDDING_BANDS = [f"EMB0{i}" for i in range(1, EMBEDDING_DIM + 1)]

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
# Fixtures
#
@pytest.fixture(scope="module")
def encoder():
    """Encoder pre-trained with the MODIS NDVI samples."""
    return sits_pre_train(
        samples=samples_modis_ndvi,
        rl_method=sits_ssl_vicreg(
            embedding_dim=EMBEDDING_DIM,
            epochs=1,
        ),
    )


@pytest.fixture(scope="module")
def embeddings(encoder):
    """MODIS NDVI samples encoded as embeddings."""
    return sits_encode(
        data=samples_modis_ndvi,
        encoder=encoder,
    )


@pytest.fixture(scope="module")
def embeddings_cube(encoder, local_cube, tmp_path_factory):
    """MODIS cube encoded as an embeddings cube."""
    return sits_encode(
        data=local_cube,
        encoder=encoder,
        output_dir=tmp_path_factory.mktemp("embeddings"),
        multicores=1,
        memsize=4,
        progress=False,
    )


#
# Test encoding of time series
#
@pytest.mark.parametrize("model_fn", ALL_ENCODER_METHODS)
def test_encode_time_series(model_fn):
    """Test time series encoding with all available encoder methods."""
    # Pre-train an encoder
    rl_model = sits_pre_train(
        samples=samples_modis_ndvi,
        rl_method=model_fn(
            embedding_dim=EMBEDDING_DIM,
            epochs=1,
        ),
    )

    # Encode the samples used to pre-train the encoder
    embeddings = sits_encode(
        data=samples_modis_ndvi,
        encoder=rl_model,
    )

    assert isinstance(embeddings, SITSTimeSeriesModel)

    # The original band (``NDVI``) is replaced by the embedding dimensions
    assert sits_bands(embeddings) == EMBEDDING_BANDS

    # The samples structure is preserved
    assert embeddings.shape[0] == samples_modis_ndvi.shape[0]
    assert sits_labels(embeddings) == sits_labels(samples_modis_ndvi)

    # Each embedding is a single point in time (the samples ``start_date``)
    assert len(sits_timeline(embeddings)) == 1


#
# Test encoding of data cubes
#
def test_encode_cube(encoder, local_cube, tmp_path: Path):
    """Test data cube encoding."""
    embeddings_cube = sits_encode(
        data=local_cube,
        encoder=encoder,
        output_dir=tmp_path,
        multicores=1,
        memsize=4,
        progress=False,
    )

    assert isinstance(embeddings_cube, SITSCubeModel)

    # The original band (``NDVI``) is replaced by the embedding dimensions
    assert sits_bands(embeddings_cube) == EMBEDDING_BANDS

    # the cube tiling is preserved
    assert embeddings_cube["tile"][0] == local_cube["tile"][0]

    # one file is written for each embedding dimension
    assert embeddings_cube["file_info"][0].shape[0] == EMBEDDING_DIM
    assert len(list(tmp_path.glob("*EMB*.tif"))) == EMBEDDING_DIM

    # Test recover
    recovered_cube = sits_encode(
        data=local_cube,
        encoder=encoder,
        output_dir=tmp_path,
        multicores=1,
        memsize=4,
        progress=False,
    )

    assert sits_bands(recovered_cube) == EMBEDDING_BANDS
    assert len(list(tmp_path.glob("*EMB*.tif"))) == EMBEDDING_DIM


#
# Test classification based on embeddings
#
def test_encode_cube_classification(embeddings, embeddings_cube, tmp_path: Path):
    """Test classification of an embeddings cube."""
    # Train a model using the encoded samples
    model = sits_train(embeddings, ml_method=sits_rfor())

    # Classify the embeddings cube
    probs_cube = sits_classify(
        data=embeddings_cube,
        ml_model=model,
        output_dir=tmp_path,
        multicores=1,
        memsize=4,
        progress=False,
    )

    assert isinstance(probs_cube, SITSCubeModel)
    assert sits_bands(probs_cube) == ["probs"]

    # Generate labels
    label_cube = sits_label_classification(probs_cube, output_dir=tmp_path)

    assert "labels" in label_cube.columns
    assert sits_labels(label_cube) == sits_labels(samples_modis_ndvi)


#
# Test encoding errors
#
def test_encode_invalid_encoder():
    """Test encoding with a model that is not an encoder."""
    ml_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor())

    with pytest.raises(RRuntimeError, match="invalid encoder"):
        sits_encode(data=samples_modis_ndvi, encoder=ml_model)


#
# Test visualization of embeddings
#
@pytest.mark.parametrize(
    "plot_args",
    [
        {},
        {"mode": "dimensions"},
        {"mode": "PCA"},
        {"mode": "tsne", "perplexity": 30},
    ],
)
def test_encode_time_series_plot(embeddings, plot_args, no_plot_window):
    """Test visualization of encoded time series."""
    sits_plot(embeddings, **plot_args)


def test_encode_time_series_plot_by_label(embeddings, no_plot_window):
    """Test visualization of encoded time series from a single label."""
    label = sits_labels(embeddings)[0]

    sits_plot(sits_select(embeddings, labels=label), mode="dimensions")


@pytest.mark.parametrize(
    "plot_args",
    [
        {},
        {"band": "EMB01"},
        {"red": "EMB04", "green": "EMB02", "blue": "EMB03"},
    ],
)
def test_encode_cube_plot(embeddings_cube, plot_args, no_plot_window):
    """Test visualization of an embeddings cube."""
    sits_plot(embeddings_cube, **plot_args)
