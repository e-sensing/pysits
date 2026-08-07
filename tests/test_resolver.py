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

"""Unit tests for class resolvers."""

import pytest
import rpy2.robjects as ro

from pysits.models.data.accuracy import SITSAccuracy
from pysits.models.data.base import SITStructureData
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.frame import SITSFrame, SITSFrameSF
from pysits.models.data.matrix import SITSConfusionMatrix, SITSMatrix
from pysits.models.data.ts import (
    SITSTimeSeriesClassificationModel,
    SITSTimeSeriesModel,
    SITSTimeSeriesSFModel,
)
from pysits.models.data.tuning import SITSTuningResults
from pysits.models.ml import SITSMachineLearningMethod
from pysits.models.resolver import accuracy_class_resolver, content_class_resolver


def r_object_as(*classes: str) -> ro.vectors.DataFrame:
    """Create an R object with the given classes."""
    data = ro.r("tibble::tibble(a = 1)")
    data.rclass = ro.StrVector(classes)

    return data


@pytest.mark.parametrize(
    ("classes", "expected_class"),
    [
        (("predicted", "sits", "tbl_df"), SITSTimeSeriesClassificationModel),
        (("sits", "tbl_df"), SITSTimeSeriesModel),
        (("raster_cube", "tbl_df"), SITSCubeModel),
        (("sits_tuned", "tbl_df"), SITSTuningResults),
        (("sf", "tbl_df"), SITSTimeSeriesSFModel),
        (("sf", "data.frame"), SITSFrameSF),
        (("tbl_df", "data.frame"), SITSFrame),
        (("matrix", "array"), SITSMatrix),
        (("sits_model", "function"), SITSMachineLearningMethod),
        (("som_map", "list"), SITStructureData),
    ],
)
def test_content_class_resolver(classes, expected_class):
    """Test content class resolution."""
    assert content_class_resolver(r_object_as(*classes)) is expected_class


@pytest.mark.parametrize(
    ("classes", "expected_class"),
    [
        (("confusionMatrix",), SITSConfusionMatrix),
        (("sits_area_accuracy", "list"), SITSAccuracy),
    ],
)
def test_accuracy_class_resolver(classes, expected_class):
    """Test accuracy class resolution."""
    assert accuracy_class_resolver(r_object_as(*classes)) is expected_class


@pytest.mark.parametrize("resolver", [content_class_resolver, accuracy_class_resolver])
def test_class_resolver_unsupported_object(resolver):
    """Test class resolution of an unsupported R object."""
    with pytest.raises(ValueError, match="Unknown or unsupported R object"):
        resolver(ro.r("1:3"))
