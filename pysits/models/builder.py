"""Data class selector."""

from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.backend.functions import r_fnc_class
from pysits.models import (
    SITSAccuracy,
    SITSConfusionMatrix,
    SITSCubeModel,
    SITSData,
    SITSFrame,
    SITSFrameSF,
    SITSTimeSeriesClassificationModel,
    SITSTimeSeriesModel,
    SITSTimeSeriesSFModel,
)


#
# Data class selector
#
def data_class_selector(data: RDataFrame) -> type[SITSFrame]:
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
        # Time-series classification data (``predicted``)
        case class_ if "predicted" in class_ and "sits" in class_:
            content_class = SITSTimeSeriesClassificationModel

        # Time-series data (``sits``)
        case class_ if "sits" in class_:
            content_class = SITSTimeSeriesModel

        # Data Cube (``raster_cube``)
        case class_ if "raster_cube" in class_:
            content_class = SITSCubeModel

        # Time-series data (``sits``) as sf
        case class_ if "sf" in class_ and "tbl_df" in class_:
            content_class = SITSTimeSeriesSFModel

        # Data frame as sf
        case class_ if "sf" in class_:
            content_class = SITSFrameSF

        # Data frame
        case class_ if "tbl_df" in class_:
            content_class = SITSFrame

    # Raise an error if no class was selected
    if not content_class:
        raise ValueError(
            "Unknown or unsupported R object: Only sits objects are supported."
        )

    return content_class


def accuracy_class_selector(data: RDataFrame) -> type[SITSData]:
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
            "Unknown or unsupported R object: Only sits objects are supported."
        )

    return content_class


def resolve_and_invoke_data_class(x: RDataFrame) -> SITSFrame:
    """Resolve data class and invoke it."""
    return data_class_selector(x)(x)


def resolve_and_invoke_accuracy_class(x: RDataFrame) -> SITSData:
    """Resolve accuracy class and invoke it."""
    return accuracy_class_selector(x)(x)
