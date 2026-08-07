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

"""Unit tests for validation operations (cube and time-series)."""

import pytest
import rpy2.robjects as ro
from pandas import DataFrame as PandasDataFrame

from pysits.models.data.accuracy import SITSAccuracy
from pysits.models.data.matrix import SITSConfusionMatrix
from pysits.models.data.table import SITSTable
from pysits.models.data.vector import SITSNamedVector
from pysits.models.resolver import resolve_and_invoke_accuracy_class
from pysits.sits.context import cerrado_2classes
from pysits.sits.ml import sits_rfor
from pysits.sits.ts import sits_sample, sits_validate

#
# Area accuracy results, as produced by ``sits_accuracy`` on a classified cube
#
R_AREA_ACCURACY = """
    local({
        labels <- c("Forest", "Pasture")

        accuracy <- list(
            error_matrix = table(
                factor(c("Forest", "Forest", "Pasture"), levels = labels),
                factor(c("Forest", "Pasture", "Pasture"), levels = labels)
            ),
            area_pixels = c(Forest = 100, Pasture = 200),
            error_ajusted_area = c(Forest = 150, Pasture = 150),
            stderr_prop = c(Forest = 0.1, Pasture = 0.2),
            stderr_area = c(Forest = 10, Pasture = 20),
            conf_interval = c(Forest = 19.6, Pasture = 39.2),
            accuracy = list(
                user = c(Forest = 0.5, Pasture = 1.0),
                producer = c(Forest = 1.0, Pasture = 0.5),
                overall = 0.75
            )
        )

        class(accuracy) <- c("sits_area_accuracy", class(accuracy))
        accuracy
    })
"""


@pytest.fixture
def area_accuracy() -> SITSAccuracy:
    """Area accuracy results."""
    return resolve_and_invoke_accuracy_class(ro.r(R_AREA_ACCURACY))


def test_sits_validate():
    """Test validate operation."""

    # Sample data
    samples = sits_sample(cerrado_2classes, frac=0.5)
    samples_validation = sits_sample(cerrado_2classes, frac=0.5)

    # Validate samples
    matrix = sits_validate(
        samples=samples, samples_validation=samples_validation, ml_method=sits_rfor()
    )

    # Check properties
    assert isinstance(matrix, SITSConfusionMatrix)
    assert isinstance(matrix.by_class, SITSNamedVector)
    assert isinstance(matrix.dots, list)
    assert isinstance(matrix.mode, str)
    assert isinstance(matrix.overall, SITSNamedVector)
    assert isinstance(matrix.table, SITSTable)

    # Check values
    assert matrix.mode == "sens_spec"
    assert matrix.positive == "Cerrado"


def test_area_accuracy_matrix(area_accuracy):
    """Test area accuracy error matrix."""
    assert isinstance(area_accuracy, SITSAccuracy)

    error_matrix = area_accuracy.error_matrix

    assert isinstance(error_matrix, SITSTable)
    assert error_matrix.index.tolist() == ["Forest", "Pasture"]
    assert error_matrix["Forest"].tolist() == [1, 0]


def test_area_accuracy_areas(area_accuracy):
    """Test area accuracy area properties."""
    for name in (
        "area_pixels",
        "error_ajusted_area",
        "stderr_prop",
        "stderr_area",
        "conf_interval",
    ):
        value = getattr(area_accuracy, name)

        assert isinstance(value, SITSNamedVector)
        assert value.columns.tolist() == ["Forest", "Pasture"]

    assert area_accuracy.area_pixels["Pasture"].tolist() == [200.0]
    assert area_accuracy.stderr_prop["Forest"].tolist() == [0.1]


def test_area_accuracy_metrics(area_accuracy):
    """Test area accuracy user, producer and overall metrics."""
    accuracy = area_accuracy.accuracy

    assert accuracy["overall"] == [0.75]
    assert isinstance(accuracy["user"], PandasDataFrame)
    assert isinstance(accuracy["producer"], PandasDataFrame)
    assert accuracy["user"]["Forest"].tolist() == [0.5]
    assert accuracy["producer"]["Forest"].tolist() == [1.0]


def test_area_accuracy_representation(area_accuracy):
    """Test area accuracy string representation."""
    assert "Area Weighted Statistics" in str(area_accuracy)
    assert str(area_accuracy) == repr(area_accuracy)
