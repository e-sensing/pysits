Estimate ensemble prediction based on list of probs cubes

Calculate an ensemble predictor based a list of probability cubes. The function
combines the output of two or more models to derive a weighted average. The
supported types of ensemble predictors are 'average' and 'uncertainty'. In the
latter case, the uncertainty cubes need to be provided using param
`uncert_cubes`.

Args:
    cubes (list[SITSCubeModel]): List of probability data cubes.
    type (str): Method to measure uncertainty. One of "average" or
        "uncertainty".
    weights (list[float]): Weights for averaging.
    memsize (int): Memory available for classification in GB (min = 1,
        max = 16384).
    multicores (int): Number of cores to be used for classification
        (min = 1, max = 2048).
    output_dir (str | pathlib.Path): Valid directory for output file.
    version (str): Version of the output.
    progress (bool): Set progress bar?
    uncert_cubes (list[SITSCubeModel]): Uncertainty cubes to be used as
        local weights when type = "uncertainty" is selected.
    **kwargs (dict): Parameters for specific functions.

Returns:
    SITSCubeModel: A combined probability cube.

Notes:
    The distribution of class probabilities produced by machine learning models
    such as random forest is quite different from that produced by deep
    learning models such as temporal CNN. Combining the result of two different
    models is recommended to remove possible bias induced by a single model.
    By default, the function takes the average of the class probabilities of
    two or more model results. If desired, users can use the uncertainty
    estimates for each results to compute the weights for each pixel. In this
    case, the uncertainties produced by the models for each pixel are used to
    compute the weights for producing the combined result.

Examples:
    from pysits import *
    import os
    import tempfile

    # create a data cube from local files
    data_dir = os.path.join(r_package_dir("extdata/raster/mod13q1", package="sits"))
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # create a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # classify a data cube using rfor model
    probs_rfor_cube = sits_classify(
        data=cube, ml_model=rfor_model, output_dir=tempfile.gettempdir(),
        version="rfor"
    )
    # create an SVM model
    svm_model = sits_train(samples_modis_ndvi, sits_svm())
    # classify a data cube using SVM model
    probs_svm_cube = sits_classify(
        data=cube, ml_model=svm_model, output_dir=tempfile.gettempdir(),
        version="svm"
    )
    # create a list of predictions to be combined
    pred_cubes = [probs_rfor_cube, probs_svm_cube]
    # combine predictions
    comb_probs_cube = sits_combine_predictions(
        pred_cubes,
        output_dir=tempfile.gettempdir()
    )
    # plot the resulting combined prediction cube
    plot(comb_probs_cube)
