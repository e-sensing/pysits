Create data cubes from image collections or local files.

This function creates data cubes from a variety of sources. Depending on the
parameters provided, it dispatches to one of several behaviors:

- STAC cube: create a data cube based on spatial and temporal restrictions
  in collections accessible by the STAC protocol (pass `roi`/`tiles`,
  `start_date`/`end_date`, etc., without `data_dir`).
- Local cube: create a data cube from files stored on a local directory,
  assuming users have downloaded the data from a known cloud collection or
  the data has been created by `sits` (pass `data_dir`).
- Results cube: create a data cube from local files produced by `sits`
  operations that generate results (such as probability cubes and class
  cubes) by passing results `bands` such as `"probs"`, `"bayes"`,
  `"variance"`, `"class"`, or `"uncertainty"`.
- Vector cube: create a data cube from local files which include a vector
  file produced by a segmentation algorithm (pass `raster_cube` and
  `vector_dir`).

Args:
    source (str): Data source: one of `"AWS"`, `"BDC"`, `"CDSE"`,
        `"DEAFRICA"`, `"DEAUSTRALIA"`, `"HLS"`, `"PLANETSCOPE"`, `"MPC"`,
        `"SDC"` or `"USGS"`. For local, results, and vector cubes, this is
        the source from which the original data was downloaded.
    collection (str): Image collection in the data source. To find out the
        supported collections, use `sits_list_collections()`.
    bands (list[str]): Spectral bands and indices to be included in the cube
        (optional). For results cubes, the results bands to be retrieved
        (`"probs"`, `"bayes"`, `"variance"`, `"class"`, `"uncertainty"`).
    tiles (list[str]): Tiles from the collection to be included in the cube.
    roi (dict | geopandas.GeoDataFrame): Region of interest (for STAC
        cubes).
    crs (str | int): The Coordinate Reference System (CRS) of the `roi`.
    start_date (str): Initial date to include images from the collection in
        the cube (optional), in YYYY-MM-DD format.
    end_date (str): Final date to include images from the collection in the
        cube (optional), in YYYY-MM-DD format.
    orbit (str): Orbit name (`"ascending"`, `"descending"`) for SAR cubes.
    platform (str): Optional parameter specifying the platform in case of
        the `"LANDSAT"` collection. Options: `Landsat-5`, `Landsat-7`,
        `Landsat-8`, `Landsat-9`.
    data_dir (str | pathlib.Path): Local directory where images are stored
        (for local and results cubes).
    raster_cube (SITSCubeModel): Raster cube to be merged with vector data
        (for vector cubes).
    vector_dir (str | pathlib.Path): Local directory where vector files are
        stored (for vector cubes).
    vector_band (str): Band for vector cube (`"segments"`, `"probs"`,
        `"class"`). This parameter is deprecated and will be removed in
        future versions; the type of vector data cube loaded is now defined
        based on the `raster_cube` object.
    labels (dict): Labels associated with the classes (for results cubes).
    parse_info (list[str]): Parsing information for local files.
    version (str): Version of the classified and/or labelled files.
    delim (str): Delimiter for parsing local files (default `"_"`).
    multicores (int): Number of workers for parallel processing (min = 1,
        max = 2048).
    memsize (int): Memory available (in GB) (for results cubes).
    progress (bool): Whether to show a progress bar.
    **kwargs (dict): Other parameters to be passed for specific cube types.

Returns:
    SITSCubeModel: A description of the contents of a data cube.

Examples:
    from pysits import *

    # Create a data cube from a local directory of files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # Show the bands available in the cube
    print(sits_bands(cube))

    # Plot the cube
    plot(cube)
