Inform label distribution of a set of time series

Describes labels in a set of time series.

Args:
    data (SITSTimeSeriesModel): Valid time series.

Returns:
    SITSFrame: A table with the frequency of each label.

Examples:
    from pysits import *

    # read a tibble with 400 samples of Cerrado and 346 samples of Pasture
    # print the labels
    sits_labels_summary(cerrado_2classes)
