Copy the images of a cube to a local directory

This function downloads the images of a cube in parallel. A region of
interest (`roi`) can be provided to crop the images and a resolution
(`res`) to resample the bands. `sits_cube_copy` is useful to improve
processing time in the regularization operation.

Args:
    cube (SITSCubeModel): A data cube.
    roi (str | pathlib.Path | geopandas.GeoDataFrame | dict): Region of
        interest. Either: 1. A path to a shapefile with polygons; 2. A
        `geopandas.GeoDataFrame`; 3. A `dict` (`"lon_min"`, `"lat_min"`,
        `"lon_max"`, `"lat_max"`) in WGS84; 4. A `dict` (`"xmin"`,
        `"xmax"`, `"ymin"`, `"ymax"`) with XY coordinates in the
        projection of the input cube.
    res (int): Output spatial resolution of the images. Default is
        `None`.
    crs (str): The Coordinate Reference System (CRS) of the roi. (see
        details below).
    n_tries (int): Number of attempts to download the same image.
        Default is 3.
    multicores (int): Number of cores for parallel downloading (min = 1,
        max = 2048).
    output_dir (str | pathlib.Path): Output directory where images will
        be saved.
    progress (bool): Show progress bar?
    **kwargs (dict): Additional parameters.

Returns:
    SITSCubeModel: Copy of input data cube.
    The main `sits` classification workflow has the following steps:
    1. `sits_cube`: selects a ARD image collection from a cloud
       provider.
    2. `sits_cube_copy`: copies an ARD image collection from a cloud
       provider to a local directory for faster processing.
    3. `sits_regularize`: create a regular data cube from an ARD image
       collection.
    4. `sits_apply`: create new indices by combining bands of a regular
       data cube (optional).
    5. `sits_get_data`: extract time series from a regular data cube
       based on user-provided labelled samples.
    6. `sits_train`: train a machine learning model based on image time
       series.
    7. `sits_classify`: classify a data cube using a machine learning
       model and obtain a probability cube.
    8. `sits_smooth`: post-process a probability cube using a spatial
       smoother to remove outliers and increase spatial consistency.
    9. `sits_label_classification`: produce a classified map by
       selecting the label with the highest probability from a smoothed
       cube.
    The `roi` parameter is used to crop cube images. To define a `roi`
    use one of:
    - A path to a shapefile with polygons;
    - A `geopandas.GeoDataFrame`;
    - A `SpatExtent` object;
    - A `dict` (`"lon_min"`, `"lat_min"`, `"lon_max"`, `"lat_max"`) in
      WGS84;
    - A `dict` (`"xmin"`, `"xmax"`, `"ymin"`, `"ymax"`) with XY
      coordinates.
    Defining a region of interest using `SpatExtent` or XY values not in
    WGS84 requires the `crs` parameter to be specified.

Examples:
    from pysits import *
    import tempfile

    # Creating a sits cube from BDC
    bdc_cube = sits_cube(
        source="BDC",
        collection="CBERS-WFI-16D",
        tiles=["007004", "007005"],
        bands=["B15", "CLOUD"],
        start_date="2018-01-01",
        end_date="2018-01-12"
    )
    # Downloading images to a temporary directory
    cube_local = sits_cube_copy(
        cube=bdc_cube,
        output_dir=tempfile.gettempdir(),
        roi={
            "lon_min": -46.5,
            "lat_min": -45.5,
            "lon_max": -15.5,
            "lat_max": -14.6
        },
        multicores=2,
        res=250
    )
