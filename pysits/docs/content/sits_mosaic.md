Mosaic classified cubes

Creates a mosaic of all tiles of a data cube. Mosaics can be created
from both regularized ARD images or from classified maps. In the case
of ARD images, a mosaic will be produced for each band/date
combination. It is better to first regularize the data cubes and then
use `sits_mosaic`.

Args:
    cube (SITSCubeModel): A data cube.
    crs (str | int): A target coordinate reference system of the raster
        mosaic. The provided crs could be a string (e.g, "EPSG:4326"
        or a proj4string), or an EPSG code number (e.g. 4326). Default
        is "EPSG:3857" - WGS 84 / Pseudo-Mercator.
    roi (str | pathlib.Path | geopandas.GeoDataFrame | dict): Region of
        interest (see below).
    multicores (int): Number of cores that will be used to crop the
        images in parallel.
    output_dir (str | pathlib.Path): Directory for output images.
    res (float): Spatial resolution of the mosaic. Default is None.
    version (str): Version of resulting image (in the case of multiple
        tests).
    progress (bool): Show progress bar? Default is True.

Returns:
    SITSCubeModel: a data cube with only one tile.

Notes:
    To define a `roi` use one of:
    - A path to a shapefile with polygons;
    - A `geopandas.GeoDataFrame`;
    - A `SpatExtent` object from `terra` package;
    - A `dict` (`"lon_min"`, `"lat_min"`, `"lon_max"`, `"lat_max"`) in
      WGS84;
    - A `dict` (`"xmin"`, `"xmax"`, `"ymin"`, `"ymax"`) with XY
      coordinates.
    The user should specify the CRS of the mosaic. We use "EPSG:3857"
    (Pseudo-Mercator) as the default.

Examples:
    from pysits import *
    import tempfile
    import geopandas as gpd
    from shapely.geometry import Polygon

    # create a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify a data cube
    probs_cube = sits_classify(
        data=cube, ml_model=rfor_model, output_dir=tempfile.gettempdir()
    )
    # smooth the probability cube using Bayesian statistics
    bayes_cube = sits_smooth(probs_cube, output_dir=tempfile.gettempdir())
    # label the probability cube
    label_cube = sits_label_classification(
        bayes_cube,
        output_dir=tempfile.gettempdir()
    )
    # create roi
    roi = gpd.GeoSeries(
        [
            Polygon([
                (-55.64768, -11.68649),
                (-55.69654, -11.66455),
                (-55.62973, -11.61519),
                (-55.64768, -11.68649)
            ])
        ],
        crs="EPSG:4326"
    )
    # crop and mosaic classified image
    mosaic_cube = sits_mosaic(
        cube=label_cube,
        roi=roi,
        crs="EPSG:4326",
        output_dir=tempfile.gettempdir()
    )
