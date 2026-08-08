Classify time series or data cubes using a trained machine learning model.

This function applies a model trained by `sits_train` to classify the input
data. Its behavior depends on the type of input provided:

- Set of time series (`SITSTimeSeriesModel`): the output is the same set of
  time series with an additional `predicted` column containing the labels
  assigned to each point.
- Regular raster data cube (`SITSCubeModel`): the output is a probability
  cube with the same tiles as the input. Each tile contains a multiband
  image in which each band holds the probability that a pixel belongs to a
  given class.
- Segmented (vector) data cube (`SITSCubeModel`, produced by
  `sits_segment`): the temporal model is applied to produce pixel-level
  probabilities and the associated vector support (`vector_info`) is
  preserved. The result is a data cube that can be passed to
  `sits_label_classification` for segment-based labeling. Segment-level
  aggregation is no longer performed by `sits_classify`; use
  `sits_label_classification` to aggregate pixel probabilities inside
  segments and assign classes.

Args:
    data (SITSTimeSeriesModel | SITSCubeModel): Input to classify. Either a
            set of time series, a regular raster data cube, or a segmented
            data cube.
    ml_model (SITSMachineLearningMethod): Model trained by `sits_train`.
    roi (geopandas.GeoDataFrame | str | pathlib.Path | dict): Region of
            interest, used for raster and vector cubes. Either a
            `geopandas.GeoDataFrame`, a shapefile, or a `dict` in WGS 84
            with named XY values ("xmin", "xmax", "ymin", "ymax") or named
            lat/long values ("lon_min", "lat_min", "lon_max", "lat_max").
    exclusion_mask (geopandas.GeoDataFrame | str | pathlib.Path): Areas to
            be excluded from the classification process, for raster and
            vector cubes. Can be defined by a `geopandas.GeoDataFrame` or by
            a shapefile.
    impute_fn: Imputation function to remove NA values.
    start_date (str): Starting date for the classification (YYYY-MM-DD
            format), for raster and vector cubes.
    end_date (str): Ending date for the classification (YYYY-MM-DD format),
            for raster and vector cubes.
    memsize (int): Memory available for classification in GB (min = 1,
            max = 16384), for raster and vector cubes.
    multicores (int): Number of cores to be used for classification
            (min = 1, max = 2048).
    gpu_memory (int): Memory available in GPU in GB (default = 4).
    batch_size (int): Batch size for GPU classification.
    block_size (dict): Size of the block read and written by each worker,
            for raster and vector cubes. A `dict` with `nrows` and `ncols`.
            Default is `None`, which computes an optimal block size from
            `memsize`, `multicores` and the internal block size of the
            raster files.
    output_dir (str | pathlib.Path): Directory for the output file, for
            raster and vector cubes.
    version (str): Version of the output, for raster and vector cubes.
    n_sam_pol (int): Deprecated (vector cubes only). Segment-level
            classification is no longer performed by `sits_classify`; use
            `sits_label_classification` for segment-based labeling.
    verbose (bool): Whether to print information about processing time
            (raster and vector cubes).
    progress (bool): Whether to show a progress bar.
    **kwargs (dict): Other parameters for specific functions.

Returns:
    SITSCubeModel | SITSTimeSeriesModel: For a set of time series, a
    `SITSTimeSeriesModel` with predicted labels for each point. For a
    regular raster cube, a `SITSCubeModel` with probabilities for each
    class. For a segmented cube, a probability cube with associated vector
    support that contains pixel-level probabilities and preserves
    `vector_info` for segment-based labeling.

Notes:
    This function collapses the R S3 methods `sits_classify.sits`,
    `sits_classify.raster_cube`, and `sits_classify.vector_cube` into a
    single Python entry point; the appropriate behavior is selected based on
    the type of `data`.

Examples:
    from pysits import *

    # Train a random forest model on a set of time series
    rfor_model = sits_train(samples_modis_ndvi, ml_model=sits_rfor())

    # Classify a set of time series
    point_ndvi = sits_select(point_mt_6bands, bands=["NDVI"])
    point_class = sits_classify(point_ndvi, ml_model=rfor_model)

    # Show the predicted labels
    plot(point_class)
