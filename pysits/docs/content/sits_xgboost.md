Train extreme gradient boosting models

This function uses the extreme gradient boosting algorithm. Boosting
iteratively adds basis functions in a greedy fashion so that each new basis
function further reduces the selected loss function. This function is a front-
end to the methods in the "xgboost" package. Please refer to the documentation
in that package for more details.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    learning_rate (float): Learning rate: scale the contribution of each
        tree by a factor of 0 < lr < 1 when it is added to the current
        approximation. Used to prevent overfitting. Default: 0.15
    min_split_loss (float): Minimum loss reduction to make a further
        partition of a leaf. Default: 1.
    max_depth (int): Maximum depth of a tree. Increasing this value makes
        the model more complex and more likely to overfit. Default: 5.
    min_child_weight (float): If the leaf node has a minimum sum of instance
        weights lower than min_child_weight, tree splitting stops. The
        larger min_child_weight is, the more conservative the algorithm is.
        Default: 1.
    max_delta_step (float): Maximum delta step we allow each leaf output to
        be. If the value is set to 0, there is no constraint. If it is set
        to a positive value, it can help making the update step more
        conservative. Default: 1.
    subsample (float): Percentage of samples supplied to a tree.
        Default: 0.8.
    nfold (int): Number of the subsamples for the cross-validation.
    nrounds (int): Number of rounds to iterate the cross-validation
        (default: 100)
    nthread (int): Number of threads (default = 6)
    early_stopping_rounds (int): Training with a validation set will stop if
        the performance doesn't improve for k rounds.
    verbose (bool): Print information on statistics during the process

Returns:
    R: Model fitted to input data (to be passed to `sits_classify`)

Notes:
    Please refer to the sits documentation available in
    https://e-sensing.github.io/sitsbook/ for detailed examples.

Examples:
    from pysits import *

    # Example of training a model for time series classification
    # Retrieve the samples for Mato Grosso
    # train a xgboost model
    ml_model = sits_train(samples_modis_ndvi, ml_method=sits_xgboost)
    # classify the point
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    # classify the point
    point_class = sits_classify(data=point_ndvi, ml_model=ml_model)
    plot(point_class)
