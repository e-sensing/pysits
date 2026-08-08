Remove NA using weighted moving average

Remove NA using weighted moving average

Args:
    data (list): A time series vector or matrix.
    k (int): Width of the moving average window. Expands to both sides
        of the center element e.g. k = 2 means 4 observations (2 left,
        2 right) are taken into account. If all observations in the
        current window are NA, the window size is automatically
        increased until there are at least 2 non-NA values present.
    weighting (str): The weighting strategy to be used. More details
        below (default is "simple").

Returns:
    R: A set of filtered time series using the imputation function.

Notes:
    The `weighting` parameter defines the weighting strategy used in the
    moving window. The strategies available are:
    - `simple` - Simple Moving Average (SMA) (default option)
    - `linear` - Linear Weighted Moving Average (LWMA)
    - `exponential` - Exponential Weighted Moving Average (EWMA)
