Retrieval of sample locations by strata for a classified cube

This function can be used in two ways: (a) When the parameter
"sampling_design" is available, it takes the cube with different labels
and a column for the sampling design table with a number of samples per
class and allocates a set of locations for each class.
(b) When the parameter "sampling_design" is not provided, the method
selects a set of locations based on a classified cube based on the
parameter "samples_per_class". This parameter should either be a `dict`
(keys are the labels of the cube) or a single value. In the latter case,
the same value is used to retrieve the samples for all classes.

Args:
    cube (SITSCubeModel): Classified cube.
    sampling_design (pandas.DataFrame): Result of `sits_sampling_design`.
    alloc (str): Allocation method chosen.
    samples_per_class (int | dict): Number of samples per class (in case
        `sampling_design` is `None`). Either a single integer (applied to
        all classes) or a `dict` keyed by class label. When keyed, keys
        must be valid class labels of the cube but do not need to cover
        all classes — only the listed classes will be sampled.
    overhead (float): Additional percentage to account for border points.
    multicores (int): Number of cores that will be used to sample the
        images in parallel.
    memsize (int): Memory available for sampling.
    shp_file (str | pathlib.Path): Name of shapefile to be saved
        (optional).
    progress (bool): Show progress bar? Default is `True`.

Returns:
    SITSFrameSF: Point object with required samples and label.

Examples:
    from pysits import *
    import tempfile

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
    # label the probability cube
    label_cube = sits_label_classification(
        probs_cube,
        output_dir=tempfile.gettempdir()
    )
    # Option 1 - select samples based on sampling design
    # estimated UA for classes
    expected_ua = {
        "Cerrado": 0.95, "Forest": 0.95,
        "Pasture": 0.95, "Soy_Corn": 0.95
    }
    # design sampling
    sampling_design = sits_sampling_design(label_cube, expected_ua)
    # select samples using the sampling design
    samples = sits_stratified_sampling(
        label_cube,
        sampling_design=sampling_design,
        alloc="alloc_prop"
    )
    # Option 2 - Select samples based on a fixed number of samples per class
    samples = sits_stratified_sampling(
        label_cube,
        samples_per_class=100
    )
