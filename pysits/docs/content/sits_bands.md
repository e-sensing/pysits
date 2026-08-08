Get the names of the bands

Finds the names of the bands of a set of time series or of a data cube

Args:
    x (SITSTimeSeriesModel | SITSCubeModel): time series or data cube.
    value (list[str]): new value for the bands.

Returns:
    list: the names of the bands.

Examples:
    from pysits import *

    # Create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # Get the bands from a data cube
    bands = sits_bands(cube)
    # Get the bands from a sits tibble
    bands = sits_bands(samples_modis_ndvi)
    # Get the bands from patterns
    bands = sits_bands(sits_patterns(samples_modis_ndvi))
    # Get the bands from ML model
    rf_model = sits_train(samples_modis_ndvi, sits_rfor())
    bands = sits_bands(rf_model)
