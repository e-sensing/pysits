Build a labelled image from a probability cube

Takes a set of classified raster layers with probabilities, and labels them
based on the maximum probability for each pixel. This function is the final
step of the main land classification workflow.
When the input is a segmented probability cube (produced by `sits_classify`
from a segmented cube), this function performs segment-based labeling:
pixel-level probabilities are aggregated inside each segment using the method
specified by `label_method`. All pixels within a segment receive the same
class label in the output raster. A GPKG file with segment summaries
(including a `class` column) is written automatically.

Args:
    cube (SITSCubeModel): Classified probability data cube (pixel-based or
        segment-based).
    memsize (int): Maximum overall memory (in GB) to label the
        classification.
    multicores (int): Number of workers to label the classification in
        parallel.
    output_dir (str | pathlib.Path): Output directory for classified files.
    version (str): Version of resulting image (in the case of multiple
        runs).
    progress (bool): Show progress bar?
    label_method (str): Decision method for segment-based labeling. One of
        "mean" (default), "median", or "majority". Only used when input is a
        segment-based probability cube.
    **kwargs (dict): Configuration parameters for exact extraction of
        segment values.

Returns:
    SITSCubeModel: A data cube with an image with the classified map. When
        input is a segment-based probability cube, the output preserves
        vector information.

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
    The OBIA workflow adds segmentation before classification:
    1. `sits_segment`: segment the raster cube to produce a vector_cube.
    2. `sits_classify`: classify pixel-level probabilities, preserving vector
       support.
    3. `sits_label_classification`: aggregate probabilities per segment and
       assign class labels.
    Please refer to the sits documentation available in
    https://e-sensing.github.io/sitsbook/ for detailed examples.

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
