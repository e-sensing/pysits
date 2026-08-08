Obtain predictors for time series samples

Predictors are X-Y values required for machine learning algorithms,
organized as a data table where each row corresponds to a training
sample. The first two columns of the predictors table are categorical
(`label_id` and `label`). The other columns are the values of each band
and time, organized first by band and then by time.

Args:
    samples (SITSTimeSeriesModel): Time series samples.

Returns:
    SITSFrame: The predictors for the sample, with one row per sample.
