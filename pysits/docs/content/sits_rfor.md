Train random forest models

Use Random Forest algorithm to classify samples. This function is a
front-end to the `randomForest` package. Please refer to the
documentation in that package for more details.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    num_trees (int): Number of trees to grow. This should not be set to
        too small a number, to ensure that every input row gets predicted
        at least a few times (default: 100, min = 20).
    mtry (int): Number of variables randomly sampled as candidates at each
        split (default: None - use default value of
        `randomForest::randomForest()` function, i.e.
        `floor(sqrt(features))`).
    classwt (dict): Assigns priors to classes, influencing the Gini index
        for splitting. Note that this parameter affects the tree-building
        process rather than just post-hoc voting.
    **kwargs (dict): Other parameters to be passed to
        `randomForest::randomForest` function.

Returns:
    SITSMachineLearningMethod: Model fitted to input data (to be passed to
        `sits_classify`).

Examples:
    from pysits import *

    # Example of training a model for time series classification
    # Retrieve the samples for Mato Grosso
    # train a random forest model
    rf_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor)
    # classify the point
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    # classify the point
    point_class = sits_classify(data=point_ndvi, ml_model=rf_model)
    plot(point_class)
