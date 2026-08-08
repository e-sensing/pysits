Get values from classified maps

Given a set of lat/long locations and a classified cube, retrieve the class of
each point. This function is useful to obtain values from classified cubes for
accuracy estimates.

Args:
    cube (SITSCubeModel): Classified data cube.
    samples (SITSTimeSeriesModel | geopandas.GeoDataFrame | str | pathlib.Path | pandas.DataFrame): Location of the
        samples to be retrieved. Either a `SITSTimeSeriesModel`, a
        `geopandas.GeoDataFrame`, the name of a shapefile or CSV file, or a
        `pandas.DataFrame` with columns "longitude" and "latitude".

Returns:
    SITSFrame: table with columns <longitude, latitude, start_date, end_date,
        label>.

Notes:
    There are four ways of specifying data to be retrieved using the `samples`
    parameter: (a) CSV file: a CSV file with columns `longitude`, `latitude`;
    (b) SHP file: a shapefile in POINT geometry; (c) a `SITSTimeSeriesModel`;
    (d) a `geopandas.GeoDataFrame` with POINT or geometry; (e) a
    `pandas.DataFrame` with `longitude` and `latitude`.

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
    # plot the probability cube
    plot(probs_cube)
    # smooth the probability cube using Bayesian statistics
    bayes_cube = sits_smooth(probs_cube, output_dir=tempdir())
    # plot the smoothed cube
    plot(bayes_cube)
    # label the probability cube
    label_cube = sits_label_classification(
        bayes_cube,
        output_dir=tempdir()
    )
    # obtain the a set of points for sampling
    ground_truth = r_package_dir("extdata/samples/samples_sinop_crop.csv", package="sits")
    # get the classification values for a selected set of locations
    labels_samples = sits_get_class(label_cube, ground_truth)
