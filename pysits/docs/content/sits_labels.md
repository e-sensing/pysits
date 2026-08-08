Get labels associated to a data set

Finds labels in a time series set or data cube

Args:
    data (SITSTimeSeriesModel | SITSTimeSeriesPatternsModel | SITSCubeModel | SITSMachineLearningMethod): time series, patterns, data cube, or trained model.

Returns:
    list: the labels of the input data.

Examples:
    from pysits import *
    import tempfile

    # get the labels for a time series set
    labels_ts = sits_labels(samples_modis_ndvi)
    # get labels for a set of patterns
    labels_pat = sits_labels(sits_patterns(samples_modis_ndvi))
    # create a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # get labels for the model
    labels_mod = sits_labels(rfor_model)
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify a data cube
    probs_cube = sits_classify(
        data=cube, ml_model=rfor_model, output_dir=tempfile.gettempdir()
    )
    # get the labels for a probs cube
    labels_probs = sits_labels(probs_cube)
