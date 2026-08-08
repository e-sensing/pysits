Return a set of time series or a data cube as a `geopandas.GeoDataFrame`.

Converts a set of time series or a data cube to a `geopandas.GeoDataFrame`.

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): a set of time series or
            a data cube.
    crs (CRS): input coordinate reference system.
    as_crs (CRS): output coordinate reference system.
    **kwargs (dict): additional parameters.

Returns:
    SITSFrame: a point or polygon geometry object.

Examples:
    from pysits import *

    # convert sits tibble to a GeoPandas object (point)
    geo_object = sits_as_geopandas(cerrado_2classes)

    # convert sits cube to a GeoPandas object (polygon)
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    geo_object = sits_as_geopandas(cube)
