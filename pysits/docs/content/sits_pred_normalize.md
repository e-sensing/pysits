Normalize predictor values

Most machine learning algorithms require data to be normalized. This
applies to the "SVM" method and to all deep learning ones. To normalize
the predictors, it is required that the statistics per band for each
sample have been obtained by the `sits_stats` function.

Args:
    pred (pandas.DataFrame): X-Y predictors, with one row per sample.
    stats (dict): Values of time series for Q02 and Q98 of the data
        (two elements).

Returns:
    SITSFrame: Normalized predictor values.

Examples:
    from pysits import *

    stats = sits_stats(samples_modis_ndvi)
    pred = sits_predictors(samples_modis_ndvi)
    pred_norm = sits_pred_normalize(pred, stats)
