Sample a time series

Takes samples from a set of time series and returns a new
`SITSTimeSeriesModel`. For a given field as a group criterion, the result
contains a percentage of the total number of samples per group. If frac > 1,
all sampling will be done with replacement.

Args:
    data (SITSTimeSeriesModel): time series.
    frac (float): percentage of samples to extract (range: 0.0 to 2.0,
        default = 0.2).
    oversample (bool): oversample classes with small number of samples?

Returns:
    SITSTimeSeriesModel: time series with a fixed quantity of samples.

Examples:
    from pysits import *

    # Retrieve a set of time series with 2 classes
    # (cerrado_2classes is available as a sample dataset)
    # Print the labels of the resulting tibble
    summary(cerrado_2classes)
    # Sample by fraction
    data_02 = sits_sample(cerrado_2classes, frac=0.2)
    # Print the labels
    summary(data_02)
