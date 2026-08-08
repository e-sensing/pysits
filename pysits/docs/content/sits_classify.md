Classify a set of time series or a data cube.

This function applies a machine learning model (trained by `sits_train`)
to classify time series or data cubes. Its behavior depends on the type
of the input `data`:

- Set of time series (`SITSTimeSeriesModel`): the output is the same set
  of time series with an additional `predicted` column containing the
  assigned labels for each point.
- Regular raster cube (`SITSCubeModel`): the output is a probability cube
  with the same tiles as the input. Each tile is a multiband image where
  each band contains the probability that a pixel belongs to a given
  class.
- Segmented (vector) data cube (produced by `sits_segment`): the temporal
  model is applied to produce pixel-level probabilities, and the
  associated vector support (`vector_info`) is preserved in the output.
  The result is a probability cube with vector support, which can then be
  passed to `sits_label_classification` for segment-based labeling.
  Segment-level aggregation is no longer performed by `sits_classify`;
  use `sits_label_classification` to aggregate pixel probabilities inside
  segments and assign classes.

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): input to classify. Either
        a set of time series, a regular raster data cube, or a segmented
        vector data cube.
    ml_model (SITSMachineLearningMethod): model trained by `sits_train`.
    roi (dict | str | pathlib.Path | geopandas.GeoDataFrame): region of
        interest, either a `geopandas.GeoDataFrame`, a shapefile, or a
        `dict` in WGS 84 with named XY values (`xmin`, `xmax`, `ymin`,
        `ymax`) or named lat/long values (`lon_min`, `lat_min`,
        `lon_max`, `lat_max`). Applies to raster and vector cubes.
    exclusion_mask (geopandas.GeoDataFrame | str | pathlib.Path): areas
        to be excluded from the classification process, defined by a
        `geopandas.GeoDataFrame` or a shapefile. Applies to raster and
        vector cubes.
    impute_fn: imputation function to remove NA.
    start_date (str): starting date for the classification (in YYYY-MM-DD
        format). Applies to raster and vector cubes.
    end_date (str): ending date for the classification (in YYYY-MM-DD
        format). Applies to raster and vector cubes.
    memsize (int): memory available for classification in GB (min = 1,
        max = 16384). Applies to raster and vector cubes.
    multicores (int): number of cores to be used for classification
        (min = 1, max = 2048).
    gpu_memory (int): memory available in GPU in GB (default = 4).
    batch_size (int): batch size for GPU classification.
    block_size (dict): size of the block read and written by each worker,
        with `[nrows, ncols]`. Default is `None`, which computes an
        optimal block size from `memsize`, `multicores` and the internal
        block size of the raster files. Applies to raster and vector
        cubes.
    output_dir (str | pathlib.Path): directory for output file. Applies
        to raster and vector cubes.
    version (str): version of the output. Applies to raster and vector
        cubes.
    n_sam_pol (int): deprecated. Segment-level classification is no longer
        performed by `sits_classify`. Use `sits_label_classification` for
        segment-based labeling. Applies to vector cubes.
    verbose (bool): print information about processing time? Applies to
        raster and vector cubes.
    progress (bool): show progress bar?
    **kwargs (dict): other parameters for specific functions.

Returns:
    SITSCubeModel: for a set of time series, a `SITSTimeSeriesModel` with
        predicted labels for each point. For a regular raster cube, a data
        cube with probabilities for each class. For a segmented vector
        cube, a probability cube with associated vector support that
        contains pixel-level probabilities and preserves `vector_info` for
        segment-based labeling.

Examples:
    from pysits import *

    # Example 1: classify a set of time series
    # create a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())

    # classify a point
    point_ndvi = sits_select(point_mt_6bands, bands=["NDVI"])
    point_class = sits_classify(data=point_ndvi, ml_model=rfor_model)
    plot(point_class)

    # Example 2: classify a raster cube
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # classify a data cube
    probs_cube = sits_classify(
        data=cube,
        ml_model=rfor_model,
        output_dir="./tempdir"
    )
    plot(probs_cube)

    # label the probability cube
    label_cube = sits_label_classification(
        probs_cube,
        output_dir="./tempdir"
    )
    plot(label_cube)
