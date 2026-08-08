Find temporal patterns associated to a set of time series

This function takes a set of time series samples as input estimates a set of
patterns. The patterns are calculated using a GAM model. The idea is to use a
formula of type y ~ s(x), where x is a temporal reference and y if the value of
the signal. For each time, there will be as many predictions as there are
sample values. The GAM model predicts a suitable approximation that fits the
assumptions of the statistical model, based on a smooth function.
This method is based on the "createPatterns" method of the R dtwSat package,
which is also described in the reference paper.

Args:
    data (SITSTimeSeriesModel): Time series.
    freq (int): Interval in days for estimates.
    formula: Formula to be applied in the estimate.
    **kwargs (dict): Any additional parameters.

Returns:
    SITSTimeSeriesPatternsModel: Time series with patterns.

Examples:
    from pysits import *

    patterns = sits_patterns(cerrado_2classes)
    plot(patterns)
