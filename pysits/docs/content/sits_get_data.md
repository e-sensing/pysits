Get time series from a data cube.

Retrieve a set of time series from a data cube and put the result in a
`SITSTimeSeriesModel`, which contains both the satellite image time
series and their metadata. The type of retrieval depends on what is
passed as the `samples` argument, which may be a CSV file, a shapefile,
a `geopandas.GeoDataFrame`, a `pandas.DataFrame`, or an existing
`SITSTimeSeriesModel`.

The `samples` argument can be one of the following:

- A CSV file (extension ".csv") with mandatory columns `longitude`,
  `latitude`, `label`, `start_date` and `end_date`.
- A `pandas.DataFrame` with mandatory columns `longitude` and
  `latitude`, and optional columns `start_date`, `end_date` and
  `label`.
- A `geopandas.GeoDataFrame` in POINT or POLYGON geometry.
- A shapefile (extension ".shp") which should be a valid shapefile in
  POINT or POLYGON geometry.
- A valid `SITSTimeSeriesModel` with columns `longitude`, `latitude`,
  `start_date`, `end_date` and `label`.

When samples are provided via `geopandas.GeoDataFrame` objects or
shapefiles and `start_date` and `end_date` are not informed, the
function uses these dates from the cube.

Args:
    cube (SITSCubeModel): Data cube from where data is to be retrieved.
    samples (SITSTimeSeriesModel | geopandas.GeoDataFrame | pandas.DataFrame | str | pathlib.Path):
        Location of the samples to be retrieved. Either a
        `SITSTimeSeriesModel`, a `geopandas.GeoDataFrame`, the name of a
        shapefile or csv file, or a `pandas.DataFrame` with columns
        `longitude` and `latitude`.
    start_date (str): Start of the interval for the time series -
        optional (date in "YYYY-MM-DD" format).
    end_date (str): End of the interval for the time series - optional
        (date in "YYYY-MM-DD" format).
    bands (list[str]): Bands to be retrieved - optional.
    impute_fn: Imputation function to remove NA.
    label (str): Label to be assigned to all time series if a `label`
        column is not provided in the samples - optional.
    label_attr (str): Attribute in the `geopandas.GeoDataFrame` or
        shapefile to be used as a polygon label.
    n_sam_pol (int): Number of samples per polygon to be read for POLYGON
        or MULTIPOLYGON objects.
    pol_avg (bool): Summarize samples for each polygon?
    sampling_type (str): Spatial sampling type: random, hexagonal,
        regular, or Fibonacci.
    crs (str): The samples CRS. Default is "EPSG:4326".
    multicores (int): Number of threads to process the time series
        (min = 1 and max = 2048).
    progress (bool): Show progress bar?
    **kwargs (dict): Specific parameters for each kind of input.

Returns:
    SITSTimeSeriesModel: The set of time series and metadata with columns
        <longitude, latitude, start_date, end_date, label, time_series>.
