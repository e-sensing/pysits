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

"""Unit tests for SOM operations."""

import pytest

from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.sits.context import samples_modis_ndvi
from pysits.sits.ts import (
    sits_som_evaluate_cluster,
    sits_som_map,
    sits_som_remove_samples,
)
from pysits.sits.utils import r_set_seed


#
# Fixtures
#
@pytest.fixture(scope="module")
def som_data():
    """SOM map and cluster evaluation of the MODIS NDVI samples."""
    r_set_seed(42)

    # Build a small SOM map, enough to expose class confusion
    som_map = sits_som_map(samples_modis_ndvi, grid_xdim=4, grid_ydim=4)

    # Return objects
    return som_map, sits_som_evaluate_cluster(som_map)


def test_som_remove_samples(som_data):
    """Test removal of samples confused with a different class."""
    som_map, som_eval = som_data

    # Remove!
    new_samples = sits_som_remove_samples(
        som_map,
        som_eval,
        "Pasture",
        "Cerrado",
    )

    # Check output type
    assert isinstance(new_samples, SITSTimeSeriesModel)

    # Only ``Cerrado`` samples are removed
    labels = samples_modis_ndvi["label"].value_counts()
    new_labels = new_samples["label"].value_counts()

    assert new_labels["Cerrado"] < labels["Cerrado"]

    # Check all other labels are there
    for label in ("Pasture", "Soy_Corn", "Forest"):
        assert new_labels[label] == labels[label]


def test_som_remove_samples_named_arguments(som_data):
    """Test removal of samples using named arguments."""
    som_map, som_eval = som_data

    # Remove samples!
    new_samples = sits_som_remove_samples(
        som_map=som_map,
        som_eval=som_eval,
        class_cluster="Pasture",
        class_remove="Cerrado",
    )

    # Same result as the positional form
    assert new_samples.shape == (
        sits_som_remove_samples(som_map, som_eval, "Pasture", "Cerrado").shape
    )


def test_som_remove_samples_unknown_label(som_data):
    """Test removal of samples using a label not available in the samples."""
    som_map, som_eval = som_data

    new_samples = sits_som_remove_samples(
        som_map,
        som_eval,
        "Pasture",
        "NotALabel",
    )

    # No samples are removed
    assert len(new_samples) == len(samples_modis_ndvi)
