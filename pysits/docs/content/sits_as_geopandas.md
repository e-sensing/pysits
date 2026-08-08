Return time series or a data cube as a `geopandas.GeoDataFrame`.

Converts time series or a data cube to a `geopandas.GeoDataFrame`.

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): time series or data
            cube.
    crs (str): input coordinate reference system.
    as_crs (str): output coordinate reference system.
    **kwargs (dict): additional parameters.

Returns:
    SITSFrame: point or polygon geometry.

Examples:
    from pysits import *

    # convert sits tibble to a geopandas object (point)
    geo_object = sits_as_geopandas(cerrado_2classes)

    # convert sits cube to a geopandas object (polygon)
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    geo_object = sits_as_geopandas(cube)
