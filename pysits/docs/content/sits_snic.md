Segment an image using SNIC

Apply a segmentation on a data cube based on the `snic` package. This is
an adaptation and extension to remote sensing data of the SNIC
superpixels algorithm proposed by Achanta and S\u00fcsstrunk (2017). See
reference for more details.

Args:
    data (pandas.DataFrame): Time series.
    grid_seeding (str): Method for grid seeding (one of "rectangular",
        "diamond", "hexagonal", "random").
    spacing (int): Distance (in number of cells) between initial
        supercells' centers.
    compactness (float): A compactness value. Larger values cause
        clusters to be more compact/even (square).
    padding (int): Distance (in pixels) from the image borders within
        which no seeds are placed.

Returns:
    R: The segmentation function to be applied to a data cube.

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
            compactness=0.5,
            padding=5
        ),
        output_dir=tempfile.mkdtemp(),
        version="snic-demo"
    )
    # create a classification model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # classify the segments
    seg_probs = sits_classify(
        data=segments,
        ml_model=rfor_model,
        output_dir=tempfile.mkdtemp(),
        version="snic-demo"
    )
    # label the probability segments
    seg_label = sits_label_classification(
        cube=seg_probs,
        output_dir=tempfile.mkdtemp(),
        version="snic-demo"
    )
    plot(seg_label)
