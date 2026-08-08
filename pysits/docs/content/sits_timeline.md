Get timeline of a cube or a set of time series

This function returns the timeline for a given data set, either a set of
time series, a data cube, or a trained model.

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): time series or data cube.

Returns:
    list: timeline of samples or data cube.

Examples:
    from pysits import *

    sits_timeline(samples_modis_ndvi)
