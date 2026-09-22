Read sits time series from the Parquet format

Reads a file written by `sits_to_parquet` and rebuilds the time series,
with its class, column order and nested series.

Files written by other programs are also read. Their class is then
inferred from the columns, which must include "longitude", "latitude",
"start_date", "end_date" and "label".

Args:
    file (str | pathlib.Path): Full path or HTTP(S) URL of the file to
        read (valid file name with extension ".parquet").

Returns:
    SITSTimeSeriesModel: Time series.

Raises:
    httpx2.HTTPError: If a remote file cannot be downloaded.

Examples:
    import tempfile
    from pysits import *

    parquet_file = tempfile.gettempdir() + "/samples.parquet"
    sits_to_parquet(samples_modis_ndvi, file=parquet_file)
    samples = sits_from_parquet(parquet_file)
