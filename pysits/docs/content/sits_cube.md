Create sits data cubes from local files or cloud-based image collections.

Builds a data cube -- a `pandas.DataFrame` describing spatial and temporal
image data -- from one of several sources. This single function handles four
distinct cases, selected by the combination of arguments you provide:

- Local raster cube: images already downloaded from a known cloud collection
  or created by `sits`, read from a local directory (`data_dir`).
- STAC cube: image collections accessible through the STAC protocol, selected
  by spatial (`roi`, `tiles`) and temporal (`start_date`, `end_date`)
  restrictions.
- Results cube: local files produced by `sits` operations that generate
  results (for example probability cubes and class cubes).
- Vector cube: local files that include a vector file produced by a
  segmentation algorithm, merged with a raster cube.

Args:
    source (str): Data source: one of `"AWS"`, `"BDC"`, `"CDSE"`,
            `"DEAFRICA"`, `"DEAUSTRALIA"`, `"HLS"`, `"PLANETSCOPE"`,
            `"MPC"`, `"SDC"` or `"USGS"`. For local, results and vector
            cubes this is the source from which the original data was
            downloaded.
    collection (str): Image collection in the data source. Use
            `sits_list_collections()` to find supported collections.
    bands (list[str]): Spectral bands and indices to include in the cube
            (optional). For a results cube these are results bands to be
            retrieved (`"probs"`, `"bayes"`, `"variance"`, `"class"`,
            `"uncertainty"`). Use `sits_list_collections()` to find the
            bands available for each STAC collection.
    tiles (list[str]): Tiles from the collection to include in the cube.
    roi (dict): Region of interest for STAC cubes.
    crs (str): The Coordinate Reference System (CRS) of the `roi`.
    start_date (str): Initial date to include images from the collection in
            the cube, in `YYYY-MM-DD` format (optional).
    end_date (str): Final date to include images from the collection in the
            cube, in `YYYY-MM-DD` format (optional).
    orbit (str): Orbit name (`"ascending"`, `"descending"`) for SAR cubes.
    platform (str): Optional parameter specifying the platform for the
            `"LANDSAT"` collection. Options: `Landsat-5`, `Landsat-7`,
            `Landsat-8`, `Landsat-9`.
    data_dir (str | pathlib.Path): Local directory where images are stored
            (local, results and vector cubes).
    labels (dict): Labels associated to the classes (results cube).
    raster_cube (SITSCubeModel): Raster cube to be merged with vector data
            (vector cube).
    vector_dir (str | pathlib.Path): Local directory where vector files are
            stored (vector cube).
    vector_band (str): Band for the vector cube (`"segments"`, `"probs"`,
            `"class"`). Deprecated and will be removed in future versions;
            the vector data cube type is now defined from the `raster_cube`
            object.
    parse_info (list[str]): Parsing information for local files.
    version (str): Version of the classified and/or labelled files (results
            and vector cubes).
    delim (str): Delimiter for parsing local files (default `"_"`).
    multicores (int): Number of workers for parallel processing
            (min = 1, max = 2048).
    memsize (int): Memory available in GB (results cube).
    progress (bool): Whether to show a progress bar.
    **kwargs (dict): Other parameters passed to specific cube types.

Returns:
    SITSCubeModel: A data cube describing the contents of the images.

Notes:
    The specific cube type is inferred from the combination of arguments.
    Local raster cubes use `data_dir`; STAC cubes use spatial and temporal
    restrictions such as `roi`, `tiles`, `start_date` and `end_date`;
    results cubes use `data_dir` together with results `bands` and
    `labels`; vector cubes use `raster_cube` together with `vector_dir`.

Examples:
    from pysits import *

    # Create a local data cube from MODIS files bundled with sits
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # Inspect the cube
    print(sits_bands(cube))
    print(sits_timeline(cube))
    plot(cube)

    # Create a STAC-based data cube restricted by tiles and dates
    s2_cube = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        tiles="20LKP",
        bands=["B05", "CLOUD"],
        start_date="2018-07-18",
        end_date="2018-08-23"
    )
    print(sits_bands(s2_cube))
