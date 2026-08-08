Cleans a classified map using a local window

Applies a modal function to clean up possible noisy pixels keeping the most
frequently values within the neighborhood. In a tie, the first value of the
vector is considered. Modal functions applied to classified cubes are useful to
remove salt-and-pepper noise in the result.

Args:
    cube (SITSCubeModel): Classified data cube.
    window_size (int): An odd integer representing the size of the sliding
        window of the modal function (min = 1, max = 15).
    memsize (int): Memory available for classification in GB (min = 1,
        max = 16384).
    multicores (int): Number of cores to be used for classification (min = 1,
        max = 2048).
    output_dir (str | pathlib.Path): Valid directory for output file.
    version (str): Version of the output file.
    progress (bool): Show progress bar?
    **kwargs (dict): Specific parameters for specialised functions.

Returns:
    SITSCubeModel: A classified map.

Notes:
    The `sits_clean` function is useful to further remove classification noise
    which has not been detected by `sits_smooth`. It improves the spatial
    consistency of the classified maps.

Examples:
    from pysits import *
    import tempfile

    rf_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor)
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify a data cube
    probs_cube = sits_classify(
        data=cube,
        ml_model=rf_model,
        output_dir=tempfile.gettempdir()
    )
    # label the probability cube
    label_cube = sits_label_classification(
        probs_cube,
        output_dir=tempfile.gettempdir()
    )
    # apply a mode function in the labelled cube
    clean_cube = sits_clean(
        cube=label_cube,
        window_size=5,
        output_dir=tempfile.gettempdir(),
        multicores=1
    )
