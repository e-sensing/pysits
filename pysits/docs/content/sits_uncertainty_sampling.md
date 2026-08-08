Suggest samples for enhancing classification accuracy

Suggest samples for regions of high uncertainty as predicted by the model. The
function selects data points that have confused an algorithm. These points
don't have labels and need be manually labelled by experts and then used to
increase the classification's training set.
This function is best used in the following context:
1. Select an initial set of samples.
2. Train a machine learning model.
3. Build a data cube and classify it using the model.
4. Run a Bayesian smoothing in the resulting probability cube.
5. Create an uncertainty cube.
6. Perform uncertainty sampling.
The Bayesian smoothing procedure will reduce the classification outliers and
thus increase the likelihood that the resulting pixels with high uncertainty
have meaningful information.

Args:
    uncert_cube (SITSCubeModel): An uncertainty cube. See
        `sits_uncertainty`.
    n (int): Number of suggested points to be sampled per tile.
    min_uncert (float): Minimum uncertainty value to select a sample.
    max_uncert (float): Maximum uncertainty value to select a sample.
        Default is Inf (no upper limit).
    sampling_window (int): Window size for collecting points (in pixels).
        The minimum window size is 10.
    multicores (int): Number of workers for parallel processing (min = 1,
        max = 2048).
    memsize (int): Maximum overall memory (in GB) to run the function.
    progress (bool): Whether to show progress bars.

Returns:
    SITSFrame: Longitude and latitude in WGS84 with locations which have
        high uncertainty and meet the minimum distance criteria.

Examples:
    from pysits import *

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
        data=cube, ml_model=rfor_model, output_dir=tempdir()
    )
    # create an uncertainty cube
    uncert_cube = sits_uncertainty(probs_cube,
        type="entropy",
        output_dir=tempdir()
    )
    # obtain a new set of samples for active learning
    # the samples are located in uncertain places
    new_samples = sits_uncertainty_sampling(
        uncert_cube,
        n=10, min_uncert=0.4
    )
