Summarize data cubes, time series, and accuracy objects.

This is a generic function. The parameters and the returned summary
depend on the specific type of input object. It handles classified
cubes, raster cubes, variance cubes, time series, and accuracy
assessment objects.

Args:
    object (SITSCubeModel | SITSTimeSeriesModel | SITSConfusionMatrix):
            The object to be summarized. Supported inputs include a
            classified cube, a raster cube, a variance cube, a set of
            time series, a sample accuracy object, or an area accuracy
            object.
    tile (str): (raster cubes only) Tile to be summarized.
    date (str): (raster cubes only) Date to be summarized.
    intervals (float): (variance cubes only) Intervals to calculate the
            quantiles.
    sample_size (int): (variance cubes only) The approximate size of
            samples to be extracted from the variance cube (by tile).
    multicores (int): (variance cubes only) Number of cores to summarize
            data (min = 1, max = 2048).
    memsize (int): (variance cubes only) Memory in GB available to
            summarize data (min = 1, max = 16384).
    quantiles (list[str]): (variance cubes only) Quantiles to be shown.
    **kwargs (dict): Further specifications for the summary, depending on
            the input type.

Returns:
    str: A summary appropriate to the input type: a summary of a
        classified cube, a data cube, a variance cube, a set of time
        series, or a sample/area accuracy assessment.

Examples:
    from pysits import *

    # Summarize a sits time series tibble
    summary(samples_modis_ndvi)

    # Train a model and produce an accuracy assessment, then summarize it
    rfor_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor())
    point_class = sits_classify(point_mt_6bands, ml_method=rfor_model)
    summary(point_class)
