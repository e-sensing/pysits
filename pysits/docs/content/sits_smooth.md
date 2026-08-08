Smooth probability cubes with spatial predictors

Takes a set of classified raster layers with probabilities, whose metadata
is created by `sits_cube`, and applies a Bayesian smoothing function.

Args:
    cube (SITSCubeModel): Probability data cube.
    window_size (int): Size of the neighborhood (min = 3, max = 21).
    neigh_fraction (float): Fraction of neighbors with high probabilities
        to be used in Bayesian inference (min = 0.1, max = 1.0).
    smoothness (int | list[int]): Estimated variance of logit of class
        probabilities (Bayesian smoothing parameter) (min = 1, max = 200).
    exclusion_mask (geopandas.GeoDataFrame | str | pathlib.Path): Areas to
        be excluded from the classification process.
    memsize (int): Memory available for classification in GB (min = 1,
        max = 16384).
    multicores (int): Number of cores to be used for classification
        (min = 1, max = 2048).
    output_dir (str | pathlib.Path): Valid directory for output file.
    version (str): Version of the output.
    progress (bool): Check progress bar?
    **kwargs (dict): Other parameters for specific functions.

Returns:
    SITSCubeModel: A data cube.

Notes:
    The main `sits` classification workflow has the following steps:
    1. `sits_cube`: selects a ARD image collection from a cloud provider.
    2. `sits_cube_copy`: copies an ARD image collection from a cloud provider
       to a local directory for faster processing.
    3. `sits_regularize`: create a regular data cube from an ARD image
       collection.
    4. `sits_apply`: create new indices by combining bands of a regular data
       cube (optional).
    5. `sits_get_data`: extract time series from a regular data cube based on
       user-provided labelled samples.
    6. `sits_train`: train a machine learning model based on image time series.
    7. `sits_classify`: classify a data cube using a machine learning model and
       obtain a probability cube.
    8. `sits_smooth`: post-process a probability cube using a spatial smoother
       to remove outliers and increase spatial consistency.
    9. `sits_label_classification`: produce a classified map by selecting the
       label with the highest probability from a smoothed cube.
    Machine learning algorithms rely on training samples that are derived from
    \h-picpicked by users to represent the desired output
    classes. Given the presence of mixed pixels in images regardless of
    resolution, and the considerable data variability within each class, these
    classifiers often produce results with misclassified pixels.
    Post-processing the results of `sits_classify` using `sits_smooth` reduces
    salt-and-pepper and border effects. By minimizing noise, `sits_smooth`
    brings a significant gain in the overall accuracy and interpretability of
    the final output.
    When applied to a `probs_cube`, `sits_smooth` uses a spatial window defined
    by the `window_size` parameter to identify neighboring pixels. When applied
    to a `probs_vector_cube`, the function uses segments to define neighbors.
    All pixels within a segment are considered neighbors. Together with
    `neigh_fraction`, this determines the fraction of pixels overlapped by the
    segment that are used in the smoothing process.

Examples:
    from pysits import *
    import tempfile

    # create an xgboost model
    xgb_model = sits_train(samples_modis_ndvi, sits_xgboost())
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify a data cube
    probs_cube = sits_classify(
        data=cube, ml_model=xgb_model, output_dir=tempfile.gettempdir()
    )
    # plot the probability cube
    plot(probs_cube)
    # smooth the probability cube using Bayesian statistics
    bayes_cube = sits_smooth(probs_cube, output_dir=tempfile.gettempdir())
    # plot the smoothed cube
    plot(bayes_cube)
    # label the probability cube
    label_cube = sits_label_classification(
        bayes_cube,
        output_dir=tempfile.gettempdir()
    )
    # plot the labelled cube
    plot(label_cube)
