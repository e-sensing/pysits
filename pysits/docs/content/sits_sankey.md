Plot class trajectories from multi-temporal classified cubes

Builds a Sankey (alluvial) diagram showing how each pixel changes class
across a sequence of classified cubes (e.g., yearly land-use/land-cover
maps of the same area). It reveals the "from-to" class dynamics over
time, which is useful to inspect transitions and multi-year
classification consistency.
The time steps can be provided in two mutually exclusive ways: as a
single multi-temporal classified cube whose timeline lives in the files
(each file is a step), or as two or more single-step classified cubes.
In both cases the tiles must be aligned across steps.

Args:
    cubes (list[SITSCubeModel]): Alternatively, the same input as a
        list: a single multi-temporal cube, or a list of single-step
        cubes. Provide either this argument or `**kwargs`, not both.
    labels (list[str]): Optional names for each step (one per cube),
        shown on the diagram x-axis. Defaults to the start year of each
        cube.
    roi (dict): Optional region of interest restricting the computation.
    legend (dict): Associates labels to colors (overrides the default
        sits colors).
    palette (str): A "cols4all" palette used for labels without an
        assigned color (default = "Set3").
    title (str): Plot title (default = "Class trajectories").
    memsize (int): Maximum memory available (in GB, default = 4).
    multicores (int): Number of cores for parallel processing
        (default = 2).
    progress (bool): Show a progress bar? (default = True).
    **kwargs (dict): Classified cubes given as separate arguments:
        either a single multi-temporal cube, or two or more single-step
        cubes (one per time step). Ignored when `cubes` is supplied.

Returns:
    None

Examples:
    from pysits import *
    import tempfile

    # train a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify and label the cube for two time steps
    probs_cube = sits_classify(cube, rfor_model, output_dir=tempfile.gettempdir())
    class_2013 = sits_label_classification(
        probs_cube, output_dir=tempfile.gettempdir(), version="v2013"
    )
    # a second classified cube for another time step
    class_2014 = sits_label_classification(
        probs_cube, output_dir=tempfile.gettempdir(), version="v2014"
    )
    # plot the Sankey diagram of class trajectories between the two steps
    sits_sankey(class_2013, class_2014, labels=["2013", "2014"])
