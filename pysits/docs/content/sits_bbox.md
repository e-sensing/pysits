Get the bounding box of the data

Obtain a vector of limits (either on lat/long for time series or in
projection coordinates in the case of cubes)

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): samples or data cube.
    crs (CRS): CRS of the time series.
    as_crs (CRS): CRS to project the resulting bounding box.
    **kwargs (dict): parameters for specific types.

Returns:
    SITSFrame: the bounding box.

Notes:
    Time series are associated with lat/long values in WGS84, while
    each data cube is associated to a cartographic projection. To
    obtain the bounding box of a data cube in a different projection
    than the original, use the `as_crs` parameter.

Examples:
    from pysits import *

    # get the bbox of a set of samples
    sits_bbox(samples_modis_ndvi)
    # get the bbox of a cube in WGS84
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    sits_bbox(cube, as_crs="EPSG:4326")
