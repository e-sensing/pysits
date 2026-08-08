Suggest high confidence samples to increase the training set.

Suggest points for increasing the training set. These points are labelled with
high confidence so they can be added to the training set. They need to have a
satisfactory margin of confidence to be selected. The input is a probability
cube. For each label, the algorithm finds out location where the machine
learning model has high confidence in choosing this label compared to all
others. The algorithm also considers a minimum distance between new labels, to
minimize spatial autocorrelation effects. This function is best used in the
following context:
1. Select an initial set of samples.
2. Train a machine learning model.
3. Build a data cube and classify it using the model.
4. Run a Bayesian smoothing in the resulting probability cube.
5. Perform confidence sampling.
The Bayesian smoothing procedure will reduce the classification outliers and
thus increase the likelihood that the resulting pixels with provide good
quality samples for each class.

Args:
    probs_cube (SITSCubeModel): A smoothed probability cube. See
        `sits_classify` and `sits_smooth`.
    n (int): Number of suggested points per class.
    min_margin (float): Minimum margin of confidence to select a sample.
    sampling_window (int): Window size for collecting points (in pixels).
        The minimum window size is 10.
    multicores (int): Number of workers for parallel processing (min = 1,
        max = 2048).
    memsize (int): Maximum overall memory (in GB) to run the function.
    progress (bool): Show progress bar?

Returns:
    SITSFrame: longitude and latitude in WGS84 with locations which have
        high uncertainty and meet the minimum distance criteria.

Examples:
    from pysits import *
    import tempfile

    # create a data cube
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # build a random forest model
    rfor_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor())
    # classify the cube
    probs_cube = sits_classify(
        data=cube, ml_model=rfor_model, output_dir=tempfile.gettempdir()
    )
    # obtain a new set of samples for active learning
    # the samples are located in uncertain places
    new_samples = sits_confidence_sampling(probs_cube)
