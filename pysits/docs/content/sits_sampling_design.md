Allocation of sample size to strata

Takes a class cube with different labels and allocates a number of sample
sizes per strata to obtain suitable values of error-adjusted area,
providing five allocation strategies.

Args:
    cube (SITSCubeModel): Classified data cube.
    expected_ua (dict): Expected values of user's accuracy.
    alloc_options (list[float]): Fixed sample allocation for rare
        classes.
    std_err (float): Standard error we would like to achieve.
    rare_class_prop (float): Proportional area limit for rare classes.

Returns:
    SITSMatrix: options to decide allocation of sample size to each
        class. This uses the same format as Table 5 of
        Olofsson et al.(2014).

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
    # estimated UA for classes
    expected_ua = {
        "Cerrado": 0.75, "Forest": 0.9,
        "Pasture": 0.8, "Soy_Corn": 0.8
    }
    sampling_design = sits_sampling_design(label_cube, expected_ua)
