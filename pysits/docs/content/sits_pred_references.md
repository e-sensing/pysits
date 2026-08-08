Obtain categorical id and predictor labels for time series samples

Predictors are X-Y values required for machine learning algorithms,
organized as a data table where each row corresponds to a training
sample. The first two columns of the predictors table are categorical
("label_id" and "label"). The other columns are the values of each band
and time, organized first by band and then by time. This function
returns the numeric values associated to each sample.

Args:
    pred (pandas.DataFrame): X-Y predictors with one row per sample.

Returns:
    list: Labels associated to training samples.

Examples:
    from pysits import *

    pred = sits_predictors(samples_modis_ndvi)
    ref = sits_pred_references(pred)
