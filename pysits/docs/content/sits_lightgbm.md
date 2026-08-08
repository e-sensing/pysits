Train light gradient boosting model

Use LightGBM algorithm to classify samples. This function is a front-end to
the `lightgbm` package. LightGBM (short for Light Gradient Boosting Machine)
is a gradient boosting framework developed by Microsoft that's designed for
fast, scalable, and efficient training of decision tree-based models. It is
widely used in machine learning for classification, regression, ranking, and
other tasks, especially with large-scale data.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    boosting_type (str): Type of boosting algorithm (default = "gbdt").
    objective (str): Aim of the classifier (default = "multiclass").
    min_samples_leaf (int): Minimal number of data in one leaf. Can be used
        to deal with over-fitting.
    max_depth (int): Limit the max depth for tree model.
    learning_rate (float): Shrinkage rate for leaf-based algorithm.
    num_iterations (int): Number of iterations to train the model.
    n_iter_no_change (int): Number of iterations without improvements until
        training stops.
    validation_split (float): Fraction of the training data for validation.
        The model will set apart this fraction and will evaluate the loss and
        any model metrics on this data at the end of each epoch.
    **kwargs (dict): Other parameters to be passed to `lightgbm::lightgbm`
        function.

Returns:
    SITSMachineLearningMethod: Model fitted to input data (to be passed to
        `sits_classify`).

Examples:
    from pysits import *

    # Example of training a model for time series classification
    # Retrieve the samples for Mato Grosso
    # train a lightgbm model
    lgb_model = sits_train(samples_modis_ndvi, ml_method=sits_lightgbm)
    # select the NDVI band
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    # classify the point
    point_class = sits_classify(data=point_ndvi, ml_model=lgb_model)
    plot(point_class)
