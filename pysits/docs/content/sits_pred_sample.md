Obtain a fraction of the predictors data frame

Many machine learning algorithms (especially deep learning) use part of the
original samples as test data to adjust its hyperparameters and to find an
optimal point of convergence using gradient descent. This function extracts a
fraction of the predictors to serve as test values for the deep learning
algorithm.

Args:
    pred (pandas.DataFrame): X-Y predictors with one row per sample.
    frac (float): Fraction of the X-Y predictors to be extracted.

Returns:
    SITSFrame: The chosen fraction of the X-Y predictors.

Examples:
    from pysits import *

    pred = sits_predictors(samples_modis_ndvi)
    pred_frac = sits_pred_sample(pred, frac=0.5)
