Calculate the variance of a probability cube

Takes a probability data cube (either a raster or a segmented
vector cube) and estimates the variance of the logit of the
probability. For a standard raster cube, this is a local sliding-window
variance. For a vector/segmented cube, it calculates the variance of all
pixels inside each segment. This supports the choice of parameters for
Bayesian smoothing.

Args:
    cube (SITSCubeModel): Probability data cube.
    window_size (int): Size of the neighborhood (odd integer). Not used
        for a segmented vector cube.
    neigh_fraction (float): Fraction of neighbors with highest
        probability for Bayesian inference (from 0.0 to 1.0).
    memsize (int): Maximum overall memory (in GB) to run the smoothing
        (min = 1, max = 16384).
    multicores (int): Number of cores to run the smoothing function
        (min = 1, max = 2048).
    output_dir (str | pathlib.Path): Output directory for image files.
    version (str): Version of resulting image.
    progress (bool): Check progress bar?
    **kwargs (dict): Parameters for specific functions.

Returns:
    SITSCubeModel: A variance data cube.

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
    # plot the probability cube
    plot(probs_cube)
    # smooth the probability cube using Bayesian statistics
    var_cube = sits_variance(probs_cube, output_dir=tempfile.gettempdir())
    # plot the variance cube
    plot(var_cube)
