Encode data using a pre-trained deep learning encoder.

Encodes either a regular raster data cube or a set of time series using a
pre-trained deep learning encoder returned by `sits_pre_train`. The
behavior depends on the type of `data` provided.

When `data` is a raster data cube, the output is an embeddings cube with
the same tiling as the input cube. Each tile is written as a multiband
raster, where each band corresponds to one embedding dimension produced
by the encoder.

When `data` is a set of time series, the output preserves the input
structure and replaces the `time_series` column with the corresponding
embeddings.

Args:
    data (SITSCubeModel | SITSTimeSeriesModel): Data to be encoded. Either
        a regular raster data cube or a set of time series.
    encoder (SITSRepresentationLearningMethod): Encoder returned by
        `sits_pre_train`.
    roi (str | pathlib.Path | geopandas.GeoDataFrame | dict): Optional
        region of interest used to restrict processing (raster cube only).
        It may be provided as: (1) a path to a polygon shapefile; (2) a
        `geopandas.GeoDataFrame` with `POLYGON` or `MULTIPOLYGON`
        geometry; (3) a named bounding box in WGS84 with `xmin`, `xmax`,
        `ymin`, `ymax`; or (4) a named lon/lat bounding box with
        `lon_min`, `lon_max`, `lat_min`, `lat_max`.
    impute_fn: Imputation function used to interpolate missing values in
        each pixel time series (default: `impute_linear`).
    start_date (str): Optional start date for temporal filtering
        (YYYY-MM-DD), raster cube only. Defaults to the cube start date.
    end_date (str): Optional end date for temporal filtering (YYYY-MM-DD),
        raster cube only. Defaults to the cube end date.
    memsize (int): Memory available for processing in GB (minimum 1),
        raster cube only.
    multicores (int): Number of CPU cores used for processing (minimum 1;
        maximum 2048 for time series).
    gpu_memory (int): GPU memory available for encoding in GB (minimum 1).
    batch_size (int): Batch size used when encoding on GPU.
    block_size (dict): Size of the block read and written by each worker
        (raster cube only). A named vector with `nrows` and `ncols`.
        Default is `None`, which computes an optimal block size from
        `memsize`, `multicores` and the internal block size of the raster
        files.
    output_dir (str | pathlib.Path): Directory where output files will be
        written (raster cube only).
    verbose (bool): If `True`, print processing time information (raster
        cube only).
    progress (bool): If `True`, show a progress bar.
    **kwargs (dict): Additional arguments passed to lower-level encoding
        routines.

Returns:
    SITSTimeSeriesModel: For a raster cube, an embeddings cube written to
    `output_dir`, with one multiband raster per tile date. For a set of
    time series, a `SITSTimeSeriesModel` with `time_series` containing the
    embeddings produced by `encoder`.
