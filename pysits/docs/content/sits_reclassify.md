Reclassify a classified cube

Reclassify a classification cube using a set of named expressions.
For classified cubes, expressions relabel pixels based on logical
conditions that may combine information from the classified cube and
an optional mask cube.
For probability cubes and probability vector cubes, expressions are
used to group input labels into new labels by aggregating
probabilities (summing probabilities of the selected input labels).

Args:
    cube (SITSCubeModel): Image cube to be reclassified (a classified
        cube, probability cube, or probability vector cube).
    mask (SITSCubeModel): Image cube with additional information to be
        used in expressions. Used only for classified cube
        reclassification.
    rules (dict): Expressions to be evaluated. For classified cubes,
        expressions must evaluate to a boolean and may refer to `cube`
        and `mask`. For probability cubes and probability vector
        cubes, each named rule selects one or more input labels (for
        example using `cube %in% c(...)`). The probabilities of the
        selected labels are summed to produce the new label given by
        the rule name.
    exclude_mask_na (bool): Should cube pixels be set to `None` when
        `None` values are found in mask pixels? (default `True`).
        Used only for classified cubes.
    memsize (int): Memory available for processing in GB (min = 1,
        max = 16384).
    multicores (int): Number of cores to be used for processing
        (min = 1, max = 2048).
    output_dir (str | pathlib.Path): Directory where files will be
        saved.
    version (str): Version of resulting image.
    progress (bool): Show progress bar?
    **kwargs (dict): Other parameters for specific methods.

Returns:
    SITSCubeModel: An object of the same type as `cube`: a classified
        cube for label cubes, or a probability cube and probability
        vector cube for probability cubes and probability vector
        cubes, respectively.

Notes:
    For classified cubes, reclassification changes the class assigned
    to each pixel based on user-defined rules. Users should refer to
    `cube` and `mask` to construct logical expressions. Expressions
    are evaluated sequentially on the original classified values;
    later rules override earlier ones.
    For probability cubes and probability vector cubes,
    reclassification is intended to group classes by combining
    probabilities. Each named rule defines a new output label. For
    each pixel, the probabilities of the selected input labels are
    summed and assigned to the corresponding output label. Rules are
    evaluated on the original probability layers.

Examples:
    from pysits import *
    import tempfile

    # Example for probs_cube: group labels by summing probabilities

    # Train a model
    rf_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor)

    # Open a cube
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # Classify cube
    probs_cube = sits_classify(
        data=cube,
        ml_model=rf_model,
        output_dir=tempfile.gettempdir(),
        version="classify"
    )

    # Reclassify probs_cube
    probs_nat_veg = sits_reclassify(
        cube=probs_cube,
        rules={
            "Cerrado": 'cube %in% c("Cerrado", "Forest")'
        },
        output_dir=tempfile.gettempdir()
    )
    plot(probs_nat_veg)

    # Example for label cube: replacement of labels

    # Open mask map
    data_dir = r_package_dir("extdata/raster/prodes", package="sits")
    prodes2021 = sits_cube(
        source="USGS",
        collection="LANDSAT-C2L2-SR",
        data_dir=data_dir,
        parse_info=[
            "X1", "X2", "tile", "start_date", "end_date",
            "band", "version"
        ],
        bands="class",
        version="v20220606",
        labels={
            "1": "Forest", "2": "Water", "3": "NonForest",
            "4": "NonForest2", "6": "d2007", "7": "d2008",
            "8": "d2009", "9": "d2010", "10": "d2011",
            "11": "d2012", "12": "d2013", "13": "d2014",
            "14": "d2015", "15": "d2016", "16": "d2017",
            "17": "d2018", "18": "r2010", "19": "r2011",
            "20": "r2012", "21": "r2013", "22": "r2014",
            "23": "r2015", "24": "r2016", "25": "r2017",
            "26": "r2018", "27": "d2019", "28": "r2019",
            "29": "d2020", "31": "r2020", "32": "Clouds2021",
            "33": "d2021", "34": "r2021"
        },
        progress=False
    )

    # Open classification map
    data_dir = r_package_dir("extdata/raster/classif", package="sits")
    ro_class = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        data_dir=data_dir,
        parse_info=[
            "X1", "X2", "tile", "start_date", "end_date",
            "band", "version"
        ],
        bands="class",
        labels={
            "1": "ClearCut_Fire", "2": "ClearCut_Soil",
            "3": "ClearCut_Veg", "4": "Forest"
        },
        progress=False
    )

    # Reclassify cube
    ro_mask = sits_reclassify(
        cube=ro_class,
        mask=prodes2021,
        rules={
            "Old_Deforestation": 'mask %in% c("d2007", "d2008", "d2009", "d2010", "d2011", "d2012", "d2013", "d2014", "d2015", "d2016", "d2017", "d2018", "r2010", "r2011", "r2012", "r2013", "r2014", "r2015", "r2016", "r2017", "r2018", "d2019", "r2019", "d2020", "r2020", "r2021")',
            "Water_Mask": 'mask == "Water"',
            "NonForest_Mask": 'mask %in% c("NonForest", "NonForest2")'
        },
        memsize=4,
        multicores=2,
        output_dir=tempfile.gettempdir(),
        version="ex_reclassify"
    )
