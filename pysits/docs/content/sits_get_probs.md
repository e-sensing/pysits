Get values from probability maps

Given a set of lat/long locations and a probability cube, retrieve the prob
values of each point. This function is useful to estimate probability
distributions and to assess the differences between classifiers.

Args:
    cube (SITSCubeModel): Probability data cube.
    samples (SITSTimeSeriesModel | geopandas.GeoDataFrame | str | pathlib.Path | pandas.DataFrame):
        Location of the samples to be retrieved. Either a
        `SITSTimeSeriesModel`, a `geopandas.GeoDataFrame` with POINT
        geometry, the location of a POINT shapefile, the location of a
        CSV file with columns "longitude" and "latitude", or a
        `pandas.DataFrame` with columns "longitude" and "latitude".
    window_size (int): Size of window around pixel (optional).
    **kwargs (dict): Additional arguments.

Returns:
    SITSFrameNested: table with columns <longitude, latitude, values> in
        case no windows are requested and <longitude, latitude, neighbors>
        in case windows are requested.

Notes:
    There are four ways of specifying data to be retrieved using the `samples`
    parameter:
    - CSV: a CSV file with columns `longitude`, `latitude`.
    - SHP: a shapefile in POINT geometry.
    - `geopandas.GeoDataFrame`: an object with POINT geometry.
    - `SITSTimeSeriesModel`: a valid set of time series.
    - `pandas.DataFrame`: with `longitude` and `latitude`.

Examples:
    from pysits import *

    # create a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify a data cube
    probs_cube = sits_classify(
        data=cube, ml_model=rfor_model, output_dir=tempdir()
    )
    # obtain the a set of points for sampling
    ground_truth = r_package_dir("extdata/samples/samples_sinop_crop.csv", package="sits")
    # get the classification values for a selected set of locations
    probs_samples = sits_get_probs(probs_cube, ground_truth)
