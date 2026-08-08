Build a regular data cube from an irregular one

Produces regular data cubes for analysis-ready data (ARD) image collections.
Analysis-ready data (ARD) collections available in AWS, MPC, USGS and DEAfrica
are not regular in space and time. Bands may have different resolutions, images
may not cover the entire time, and time intervals are not regular. For this
reason, subsets of these collection need to be converted to regular data cubes
before further processing and data analysis. This function requires users to
include the cloud band in their ARD-based data cubes. This function uses the
`gdalcubes` package.

Args:
    cube (SITSCubeModel): data cube whose observation period and/or spatial
        resolution is not constant.
    period (str): ISO8601-compliant time period for regular data cubes, with
        number and unit, where "D", "M" and "Y" stand for days, month and
        year; e.g., "P16D" for 16 days.
    res (float): Spatial resolution of regularized images (in meters).
    output_dir (str | pathlib.Path): Valid directory for storing regularized
        images.
    timeline (list[str]): User-defined timeline for regularized cube.
    roi (dict | geopandas.GeoDataFrame | str | pathlib.Path): Region of
        interest (see notes below).
    crs (str | int): Coordinate Reference System (CRS) of the roi. (see
        details below).
    tiles (list[str]): Tiles to be produced.
    grid_system (str): Grid system to be used for the output images.
    multicores (int): Number of cores used for regularization; used for
        parallel processing of input.
    progress (bool): show progress bar?
    **kwargs (dict): Additional parameters.

Returns:
    SITSCubeModel: A data cube with aggregated images.

Notes:
    The main `sits` classification workflow has the following steps:
    1. `sits_cube`: selects a ARD image collection from a cloud provider.
    2. `sits_cube_copy`: copies an ARD image collection from a cloud provider
       to a local directory for faster processing.
    3. `sits_regularize`: create a regular data cube from an ARD image
       collection.
    4. `sits_apply`: create new indices by combining bands of a regular data
       cube (optional).
    5. `sits_get_data`: extract time series from a regular data cube based on
       user-provided labelled samples.
    6. `sits_train`: train a machine learning model based on image time series.
    7. `sits_classify`: classify a data cube using a machine learning model and
       obtain a probability cube.
    8. `sits_smooth`: post-process a probability cube using a spatial smoother
       to remove outliers and increase spatial consistency.
    9. `sits_label_classification`: produce a classified map by selecting the
       label with the highest probability from a smoothed cube.
    The regularization operation converts subsets of image collections
    available in cloud providers into regular data cubes. It is an essential
    part of the `sits` workflow. The input to `sits_regularize` should be an
    ARD cube which includes the cloud band. The aggregation method used in
    `sits_regularize` sorts the images based on cloud cover, putting images
    with the least clouds at the top of the stack. Once the stack of images is
    sorted, the method uses the first valid value to create the temporal
    aggregation.
    The "period" parameter is mandatory, and defines the time interval between
    two images of the regularized cube. When combining Sentinel-1A and
    Sentinel-1B images, experiments show that a 16-day period ("P16D") are a
    good default. Landsat images require a longer period of one to three
    months.
    By default, the date of the first image of the input cube is taken as the
    starting date for the regular cube. In many situations, users may want to
    pre-define the required times using the "timeline" parameter. The
    "timeline" parameter, if used, must contain a set of dates which are
    compatible with the input cube.
    To define a `roi` use one of:
    - A path to a shapefile with polygons;
    - A `geopandas.GeoDataFrame`;
    - A `SpatExtent` object from `terra` package;
    - A `dict` (`"lon_min"`, `"lat_min"`, `"lon_max"`, `"lat_max"`) in
      WGS84;
    - A `dict` (`"xmin"`, `"xmax"`, `"ymin"`, `"ymax"`) with XY
      coordinates.
    Defining a region of interest using `SpatExtent` or XY values not in WGS84
    requires the `crs` parameter to be specified. `sits_regularize()` function
    will crop the images that contain the region of interest(). NOTE: Make sure
    to inform `roi` with valid geometries. `sits` will drop the use of `roi` if
    it contains invalid geometries.
    The optional `tiles` parameter indicates which tiles of the input cube will
    be used for regularization. When `grid_system` is informed, `tiles` may be
    combined with `roi` to further restrict which target grid tiles are
    produced (only tiles that both intersect `roi` and are listed in `tiles`
    are kept).
    The `grid_system` parameter allows the user to reproject the files to a
    grid system which is different from that used in the ARD image collection
    of the could provider. Currently, the package supports the use of MGRS grid
    system and those used by the Brazil Data Cube ("BDC_LG_V2" "BDC_MD_V2"
    "BDC_SM_V2").

Examples:
    from pysits import *
    import tempfile

    # define a non-regular Sentinel-2 cube in AWS
    s2_cube_open = sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        tiles=["20LKP", "20LLP"],
        bands=["B8A", "CLOUD"],
        start_date="2018-10-01",
        end_date="2018-11-01"
    )
    # regularize the cube
    rg_cube = sits_regularize(
        cube=s2_cube_open,
        period="P16D",
        res=60,
        multicores=2,
        output_dir=tempfile.gettempdir()
    )

    ## Sentinel-1 SAR
    roi = {
        "lon_min": -50.410, "lon_max": -50.379,
        "lat_min": -10.1910, "lat_max": -10.1573
    }
    s1_cube_open = sits_cube(
        source="MPC",
        collection="SENTINEL-1-GRD",
        bands=["VV", "VH"],
        orbit="descending",
        roi=roi,
        start_date="2020-06-01",
        end_date="2020-09-28"
    )
    # regularize the cube
    rg_cube = sits_regularize(
        cube=s1_cube_open,
        period="P12D",
        res=60,
        roi=roi,
        multicores=2,
        output_dir=tempfile.gettempdir()
    )
