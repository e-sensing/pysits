Assess classification accuracy

This function calculates the accuracy of the classification result. The
input is either a set of classified time series or a classified data cube.
Classified time series are produced by `sits_classify`. Classified images
are generated using `sits_classify` followed by
`sits_label_classification`.
For a set of time series, `sits_accuracy` creates a confusion matrix and
calculates the resulting statistics. For a classified image, the function
uses an area-weighted technique proposed by Olofsson et al. according to
references [1-3] to produce reliable accuracy estimates at 95% confidence
level. In both cases, it provides an accuracy assessment of the
classified, including Overall Accuracy, Kappa, User's Accuracy, Producer's
Accuracy and error matrix (confusion matrix).

Args:
    data (SITSCubeModel | SITSTimeSeriesModel): Either a data cube with
        classified images or a set of time series.
    prediction_attr (str): Name of the column of the segments that contains
        the predicted values (only for vector class cubes).
    reference_attr (str): Name of the column of the segments that contains
        the reference values (only for vector class cubes).
    validation (str | pathlib.Path | pandas.DataFrame | geopandas.GeoDataFrame | SITSTimeSeriesModel):
        Samples for validation (see below). Only required when data is a
        raster class cube.
    method (str): Either 'olofsson' or 'pixel' to compute accuracy (only
        for raster class cubes).
    **kwargs (dict): Specific parameters.

Returns:
    SITSData: The error_matrix, the class_areas, the unbiased estimated
    areas, the standard error areas, confidence interval 95 and the
    accuracy (user, producer, and overall), or `None` if the data is
    empty. The result can be visualized directly on the screen.

Notes:
    The `validation` data needs to contain the following columns:
    "latitude", "longitude", "start_date", "end_date", and "label". It can
    be either a path to a CSV file, a `SITSTimeSeriesModel`, a
    `pandas.DataFrame`, or a `geopandas.GeoDataFrame`.
    When `validation` is a `geopandas.GeoDataFrame`, the columns "latitude"
    and "longitude" are not required as the locations are extracted from the
    geometry column. The `centroid` is calculated before extracting the
    location values for any geometry type.

Examples:
    from pysits import *
    import tempfile

    # show accuracy for a set of samples
    train_data = sits_sample(samples_modis_ndvi, frac=0.5)
    test_data = sits_sample(samples_modis_ndvi, frac=0.5)
    rfor_model = sits_train(train_data, sits_rfor())
    points_class = sits_classify(
        data=test_data, ml_model=rfor_model
    )
    acc = sits_accuracy(points_class)

    # show accuracy for a data cube classification
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
        data=cube, ml_model=rfor_model, output_dir=tempfile.gettempdir()
    )
    # label the probability cube
    label_cube = sits_label_classification(
        probs_cube,
        output_dir=tempfile.gettempdir()
    )
    # obtain the ground truth for accuracy assessment
    ground_truth = r_package_dir("extdata/samples/samples_sinop_crop.csv", package="sits")
    # make accuracy assessment
    as_ = sits_accuracy(label_cube, validation=ground_truth)
