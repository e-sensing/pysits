Export sits time series to the Parquet format

Writes a set of time series to a Parquet file. The layout is long: one
row per sample and date, with the time series as plain columns. The
file metadata keeps what is needed to rebuild the data with
`sits_from_parquet` (class, column order and bands). It also follows
GeoParquet 1.1, so tools like GDAL and QGIS read the file as points.

Args:
    data (SITSTimeSeriesModel): Time series.

    file (str | pathlib.Path): Full path of the exported file (valid
        file name with extension ".parquet").

Returns:
    None

Examples:
    import tempfile
    from pysits import *

    parquet_file = tempfile.gettempdir() + "/samples.parquet"
    sits_to_parquet(samples_modis_ndvi, file=parquet_file)
