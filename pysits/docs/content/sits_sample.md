Sample a time series

Takes samples from a set of time series and returns a new
`SITSTimeSeriesModel`. For a given field as a group criterion, the
result contains a percentage of the total number of samples per group.
If frac > 1, all sampling will be done with replacement.

Args:
    data (SITSTimeSeriesModel): Set of time series.
    frac (float): Percentage of samples to extract (range: 0.0 to 2.0,
        default = 0.2).
    oversample (bool): Oversample classes with small number of samples?

Returns:
    SITSTimeSeriesModel: A set of time series with a fixed quantity of
        samples.

Examples:
    from pysits import *

    # Retrieve a set of time series with 2 classes (cerrado_2classes)
    # Print the labels of the resulting tibble
    print(sits_labels_summary(cerrado_2classes))
    # Sample by fraction
    data_02 = sits_sample(cerrado_2classes, frac=0.2)
    # Print the labels
    print(sits_labels_summary(data_02))
