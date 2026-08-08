Export sits time series metadata to the CSV format

Converts metadata from a set of time series to a CSV file. The CSV file
will not contain the actual time series. Its columns will be the same as
those of a CSV file used to retrieve data from ground information
("latitude", "longitude", "start_date", "end_date", "cube", "label").
If the file is `None`, returns a `SITSFrame` as an object.

Args:
    data (SITSTimeSeriesModel): Time series.
    file (str | pathlib.Path): Full path of the exported CSV file (valid
        file name with extension ".csv").

Returns:
    SITSFrame: Data with CSV columns (optional).

Examples:
    import tempfile
    from pysits import *

    csv_file = tempfile.gettempdir() + "/cerrado_2classes.csv"
    sits_to_csv(cerrado_2classes, file=csv_file)
