Get time series from a data cube.

Retrieve a set of time series from a data cube and put the result in a
`SITSTimeSeriesModel`, which contains both the satellite image time
series and their metadata. The samples to be retrieved can be provided
in several forms, and the accepted parameters vary slightly depending
on the type of `samples`.

The `samples` parameter may be one of the following:

- A path to a CSV file (extension ".csv") with mandatory columns
  `longitude`, `latitude`, `label`, `start_date` and `end_date`.
- A `pandas.DataFrame` with mandatory columns `longitude` and
  `latitude`, and optional columns `start_date`, `end_date` and
  `label`.
- A `geopandas.GeoDataFrame` in POINT or POLYGON geometry.
- A path to a shapefile (extension ".shp") that is a valid POINT or
  POLYGON shapefile.
- A valid `SITSTimeSeriesModel` with columns `longitude`, `latitude`,
  `start_date`, `end_date` and `label`.

For spatial inputs (`geopandas.GeoDataFrame` objects and shapefiles),
if `start_date` and `end_date` are not informed, the function uses
these dates from the cube.

Args:
    cube (SITSCubeModel): Data cube from where data is to be retrieved.
    samples (SITSTimeSeriesModel | geopandas.GeoDataFrame | pandas.DataFrame | str | pathlib.Path): Location of the samples
        to be retrieved. Either a `SITSTimeSeriesModel`, a
        `geopandas.GeoDataFrame`, the name of a shapefile or csv file,
        or a `pandas.DataFrame` with columns "longitude" and
        "latitude".
    bands (list[str]): Bands to be retrieved - optional.
    start_date (str): Start of the interval for the time series -
        optional (date in "YYYY-MM-DD" format). Applies to
        `pandas.DataFrame`, `geopandas.GeoDataFrame` and shapefile
        inputs.
    end_date (str): End of the interval for the time series - optional
        (date in "YYYY-MM-DD" format). Applies to `pandas.DataFrame`,
        `geopandas.GeoDataFrame` and shapefile inputs.
    label (str): Label to be assigned to all time series if a `label`
        column is not provided in the input.
    label_attr (str): Attribute in the `geopandas.GeoDataFrame` or
        shapefile to be used as a polygon label.
    n_sam_pol (int): Number of samples per polygon to be read for
        POLYGON or MULTIPOLYGON inputs.
    pol_avg (bool): Summarize samples for each polygon?
    sampling_type (str): Spatial sampling type: random, hexagonal,
        regular, or Fibonacci.
    crs (str): The samples CRS. Default is "EPSG:4326".
    impute_fn: Imputation function to remove NA.
    multicores (int): Number of threads to process the time series
        (with min = 1 and max = 2048).
    progress (bool): Show progress bar?
    **kwargs (dict): Specific parameters for each kind of input.

Returns:
    SITSTimeSeriesModel: The set of time series and metadata:
        <longitude, latitude, start_date, end_date, label,
        time_series>.

Examples:
    from pysits import *
    import pandas as pd

    # reading a lat/long from a local cube
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    raster_cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # obtain a set of samples defined by a lat/long point
    samples = pd.DataFrame({
        "longitude": [-55.66738],
        "latitude": [-11.76990]
    })
    points = sits_get_data(cube=raster_cube, samples=samples)
    print(points)
