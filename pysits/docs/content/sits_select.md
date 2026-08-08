Filter a data set for bands, tiles, and dates

Filter the bands, tiles, dates and labels from a set of time series or
from a data cube.

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): time series or data
        cube.
    bands (list[str]): names of the bands.
    start_date (str): date in YYYY-MM-DD format: start date to be
        filtered.
    end_date (str): date in YYYY-MM-DD format: end date to be
        filtered.
    dates (list[str]): sparse dates to be selected.
    labels (list[str]): sparse labels to be selected (only applied
        for time series data).
    tiles (list[str]): names of the tiles.
    **kwargs (dict): additional parameters to be provided.

Returns:
    SITSFrame: time series or data cube.

Examples:
    from pysits import *

    # Retrieve a set of time series with 2 classes
    # (cerrado_2classes is available directly)
    # Print the original bands
    print(sits_bands(cerrado_2classes))
    # Select only the NDVI band
    data = sits_select(cerrado_2classes, bands=["NDVI"])
    # Print the labels of the resulting tibble
    print(sits_bands(data))
    # select start and end date
    point_2010 = sits_select(point_mt_6bands,
        start_date="2000-09-13",
        end_date="2017-08-29"
    )
