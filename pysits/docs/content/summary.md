Summarize sits objects and data cubes.

This is a generic function that produces a summary of the input object.
The behavior and available parameters depend on the specific type of
object provided. It can summarize time series, raster cubes, classified
cubes, variance cubes, and accuracy assessments.

Args:
    object (SITSTimeSeriesModel | SITSCubeModel | SITSConfusionMatrix):
            The object to be summarized. Supported types include: a set
            of time series; a raster data cube; a classified data cube;
            a variance data cube; an accuracy matrix for training data;
            or an accuracy matrix for area data.
    **kwargs (dict): Further specifications for the summary. The
            accepted keyword arguments depend on the type of `object`:

            For a raster data cube:
                tile: Tile to be summarized.
                date: Date to be summarized.

            For a variance data cube:
                intervals: Intervals to calculate the quantiles.
                sample_size: The approximate size of samples that
                    will be extracted from the variance cube (by
                    tile).
                multicores: Number of cores to summarize data
                    (min = 1, max = 2048).
                memsize: Memory in GB available to summarize data
                    (min = 1, max = 16384).
                quantiles: Quantiles to be shown.

Returns:
    str: A summary of the input object. Depending on the input type,
        this is a summary of the time series, the raster data cube, the
        classified data cube, the variance data cube, or the
        sample/area accuracy.
