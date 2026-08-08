Export a full sits time series to the CSV format

Converts metadata and data from a set of time series to a CSV file.
The CSV file will not contain the actual time series. Its columns will
be the same as those of a CSV file used to retrieve data from ground
information ("latitude", "longitude", "start_date", "end_date",
"cube", "label"), plus all the time series for each data

Args:
    data (SITSTimeSeriesModel): Time series.
    file (str | pathlib.Path): Full path of the exported CSV file (valid
        file name with extension ".csv").

Returns:
    None

Examples:
    from pysits import *
    import tempfile

    csv_ts = sits_timeseries_to_csv(cerrado_2classes)
    csv_file = tempfile.gettempdir() + "/cerrado_2classes_ts.csv"
    sits_timeseries_to_csv(cerrado_2classes, file=csv_file)
