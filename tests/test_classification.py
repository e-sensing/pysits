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

"""end-to-end classification test."""

from pathlib import Path

from pysits.sits.classification import (
    sits_classify,
    sits_label_classification,
    sits_smooth,
)
from pysits.sits.context import samples_modis_ndvi
from pysits.sits.cube import sits_cube
from pysits.sits.data import sits_labels
from pysits.sits.ml import sits_rfor, sits_train
from pysits.sits.utils import get_package_dir


def test_basic_classification(tmp_path: Path):
    """Test basic classification."""
    # Train a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())

    # Create a data cube from local files
    data_dir = get_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(source="BDC", collection="MOD13Q1-6.1", data_dir=data_dir)

    # Classify a data cube
    probs_cube = sits_classify(data=cube, ml_model=rfor_model, output_dir=tmp_path)

    # Smooth the probability cube using Bayesian statistics
    bayes_cube = sits_smooth(probs_cube, output_dir=tmp_path)

    # Label the probability cube
    label_cube = sits_label_classification(bayes_cube, output_dir=tmp_path)

    # Validate result
    assert "labels" in label_cube.columns
    assert len(sits_labels(label_cube)) > 0
    assert label_cube["file_info"].shape[0] == 1
