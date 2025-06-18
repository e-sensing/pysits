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

"""Class resolvers."""

from typing import Any

from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.backend.functions import r_fnc_class
from pysits.models.data.accuracy import SITSAccuracy
from pysits.models.data.base import SITSBase, SITSData, SITStructureData
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


#
# Data class resolver
#
def content_class_resolver(data: Any) -> type[SITSBase]:
    """Select the correct SITS class for the given content.

    Args:
        data (Any): R Object.

    Returns:
        type[SITSFrame]: SITS Frame class.
    """
    # Get content class
    rds_class = r_fnc_class(data)

    # Check class
    content_class = None

    match rds_class:
        # Time-series classification data (``predicted``)
        case class_ if "predicted" in class_ and "sits" in class_:
            content_class = SITSTimeSeriesClassificationModel

        # Time-series data (``sits``)
        case class_ if "sits" in class_:
            content_class = SITSTimeSeriesModel

        # Data Cube (``raster_cube``)
        case class_ if "raster_cube" in class_:
            content_class = SITSCubeModel

        # Tuning results (``sits_tuned``)
        case class_ if "sits_tuned" in class_:
            content_class = SITSTuningResults

        # Time-series data (``sits``) as sf
        case class_ if "sf" in class_ and "tbl_df" in class_:
            content_class = SITSTimeSeriesSFModel

        # Data frame as sf
        case class_ if "sf" in class_:
            content_class = SITSFrameSF

        # Data frame
        case class_ if "tbl_df" in class_ or "data.frame" in class_:
            content_class = SITSFrame

        # Matrix
        case class_ if "matrix" in class_:
            content_class = SITSMatrix

        # ML model (any `sits_model`, including `random forest`, `svm`, `ltae`, etc.)
        case class_ if "sits_model" in class_:
            content_class = SITSMachineLearningMethod

        # SOM map (``som_map``)
        case class_ if "som_map" in class_:
            content_class = SITStructureData

    # Raise an error if no class was selected
    if not content_class:
        raise ValueError(
            "Unknown or unsupported R object: Only sits-related objects are supported."
        )

    return content_class


def accuracy_class_resolver(data: RDataFrame) -> type[SITSData]:
    """Select the correct SITS class for the data.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.

    Returns:
        SITSFrame: R Data Frame as SITS Frame.
    """
    # Get content class
    rds_class = r_fnc_class(data)

    # Check class
    content_class = None

    match rds_class:
        # Confusion matrix
        case class_ if "confusionMatrix" in class_:
            content_class = SITSConfusionMatrix

        # Area accuracy
        case class_ if "sits_area_accuracy" in class_:
            content_class = SITSAccuracy

    # Raise an error if no class was selected
    if not content_class:
        raise ValueError(
            "Unknown or unsupported R object: Only sits-related objects are supported."
        )

    return content_class


def resolve_and_invoke_content_class(x: Any) -> SITSBase:
    """Resolve data class and invoke it."""
    return content_class_resolver(x)(x)


def resolve_and_invoke_accuracy_class(x: RDataFrame) -> SITSData:
    """Resolve accuracy class and invoke it."""
    return accuracy_class_resolver(x)(x)
