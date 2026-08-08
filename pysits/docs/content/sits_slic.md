Segment an image using SLIC

Apply a segmentation on a data cube using either the `supercells` or `snic`
packages, depending on the chosen algorithm. As of version 1.5.4, two
segmentation methods are supported. The recommended option is SNIC, implemented
via the `snic` package, which applies a non-iterative clustering strategy to
generate compact, homogeneous superpixels from uniformly distributed seeds
(Achanta and Susstrunk, 2017). The alternative method uses the SLIC algorithm
implemented in the `supercells` package, adapted for remote sensing data
following Achanta et al. (2012). This SLIC variant is deprecated and will be
removed in a future release. See references for more details.

Args:
    data (SITSMatrix): time series values.
    step (int): distance (in number of cells) between initial supercells'
        centers.
    compactness (float): compactness value. Larger values cause clusters to
        be more compact/even (square).
    dist_fun (str): distance function. Currently implemented: `euclidean,
        jsd, dtw`, and any distance function from the `philentropy` package.
        See `philentropy::getDistMethods()`.
    avg_fun (str): averaging function to calculate the values of the
        supercells' centers. Accepts any fitting function (e.g., mean or
        median) or one of internally implemented "mean" and "median".
        Default: "median".
    iter (int): number of iterations to create the output.
    minarea (int): minimal size of a supercell (in cells).
    verbose (bool): show the progress bar?

Returns:
    R: set of segments for a single tile.

Examples:
    from pysits import *
    import tempfile

    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    # create a data cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # segment the vector cube
    segments = sits_segment(
        cube=cube,
        seg_fn=sits_snic(
            grid_seeding="rectangular",
            spacing=10,
            compactness=0.3,
            padding=0
        ),
        output_dir=tempfile.gettempdir(),
        version="snic-demo"
    )
    # create a classification model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # classify the segments
    seg_probs = sits_classify(
        data=segments,
        ml_model=rfor_model,
        output_dir=tempfile.gettempdir(),
        version="snic-demo"
    )
    # label the probability segments
    seg_label = sits_label_classification(
        cube=seg_probs,
        output_dir=tempfile.gettempdir(),
        version="snic-demo"
    )
    plot(seg_label)
