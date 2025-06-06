"""Data class selector."""

from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.backend.functions import r_fnc_class
from pysits.models import (
    SITSCubeModel,
    SITSFrame,
    SITSTimeSeriesClassificationModel,
    SITSTimeSeriesModel,
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

        case class_ if "tbl_df" in class_:
            content_class = SITSFrame

    # Raise an error if no class was selected
    if not content_class:
        raise ValueError(
            "Unknown or unsupported R object: Only sits objects are supported."
        )

    return content_class


def resolve_and_invoke_data_class(x: RDataFrame) -> SITSFrame:
    """Resolve data class and invoke it."""
    return data_class_selector(x)(x)
