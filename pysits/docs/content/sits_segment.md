Segment an image

Apply a spatial-temporal segmentation on a data cube based on a user defined
segmentation function. The function applies the segmentation algorithm "seg_fn"
to each tile. The output is a vector data cube, which is a data cube with an
additional vector file in "geopackage" format.

Args:
    cube (SITSCubeModel): Regular data cube.
    seg_fn: Function to apply the segmentation.
    roi (dict | str | pathlib.Path | geopandas.GeoDataFrame): Region of
        interest (see below).
    impute_fn: Imputation function to remove NA values.
    start_date (str): Start date for the segmentation.
    end_date (str): End date for the segmentation.
    memsize (int): Memory available for classification (in GB).
    multicores (int): Number of cores to be used for classification.
    output_dir (str | pathlib.Path): Directory for output file.
    version (str): Version of the output (for multiple segmentations).
    progress (bool): Show progress bar?
    **kwargs (dict): Additional arguments.

Returns:
    SITSCubeModel: The segmentation as a vector data cube.

Notes:
    Segmentation requires the following steps:
    1. Create a regular data cube with `sits_cube` and `sits_regularize`;
    2. Run `sits_segment` to obtain a vector data cube with polygons that
       define the boundary of the segments;
    3. Classify the time series associated to the segments with
       `sits_classify`, to get obtain a vector probability cube;
    4. Use `sits_label_classification` to label the vector probability cube;
    5. Display the results with `plot` or `sits_view`.
    The "roi" parameter defines a region of interest. It can be a
    `geopandas.GeoDataFrame`, a shapefile, or a bounding box `dict` with named
    XY values ("xmin", "xmax", "ymin", "ymax") or named lat/long values
    ("lon_min", "lat_min", "lon_max", "lat_max").
    As of version 1.5.4, two segmentation functions are available. The
    preferred option is `sits_snic`, which implements the Simple Non-Iterative
    Clustering (SNIC) algorithm to generate compact and homogeneous superpixels
    directly from uniformly distributed seeds. SNIC avoids the iterative
    refinement step used in SLIC and is generally faster and more memory-
    efficient, making it suitable for large multispectral or multitemporal data
    cubes.
    The previous function `sits_slic`, based on the Simple Linear Iterative
    Clustering (SLIC) algorithm as adapted by Nowosad and Stepinski for
    multispectral and multitemporal imagery, remains available but is now
    deprecated and will be removed in a future release. SLIC clusters pixels
    using spectral similarity and spatial–temporal proximity to produce nearly
    uniform superpixels, but its iterative nature makes it less efficient for
    large-scale Earth observation workflows.
    The result of `sits_segment` is a data cube with an additional vector file
    in the `geopackage` format. The location of the vector file is included in
    the data cube in a new column, called `vector_info`.

Examples:
    from pysits import *
    import tempfile

    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    # create a data cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # segment the vector cube
    segments = sits_segment(
        cube=cube,
        seg_fn=sits_snic(
            grid_seeding="diamond",
            spacing=15,
            compactness=0.5,
            padding=2
        ),
        output_dir=tempfile.mkdtemp()
    )
    # create a classification model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # classify the segments
    seg_probs = sits_classify(
        data=segments,
        ml_model=rfor_model,
        output_dir=tempfile.mkdtemp()
    )
    # label the probability segments
    seg_label = sits_label_classification(
        cube=seg_probs,
        output_dir=tempfile.mkdtemp()
    )
