Plot sits objects.

Unified plotting function that dispatches on the type of the object passed
as `x`. It mirrors the many `plot` methods of the R `sits` package,
covering data cubes (raster, SAR, DEM, vector, RGB), probability and
uncertainty cubes, variance cubes, classified images, time series patterns
and predictions, machine learning / deep learning models, clustering and
self-organizing map (SOM) results, accuracy tables, and t-SNE / embedding
visualizations. The set of accepted keyword arguments depends on the type
of object being plotted.

Args:
    x (SITSCubeModel | SITSTimeSeriesModel | SITSTimeSeriesPatternsModel | SITSMachineLearningMethod | SITSConfusionMatrix): Object to be
        plotted. Supported objects include classified raster images,
        classified segments, digital elevation model cubes, multi-year
        land use/cover embedding predictions, sample distances, class
        temporal patterns, probability cubes, raster, SAR, and vector
        data cubes, confusion matrices / accuracy metrics, dendrograms,
        trained models, time series predictions, t-SNE projections, SOM
        results, uncertainty cubes, and variance cubes.
    y: Ignored. Present for compatibility with the generic `plot`.
    band (str): Band used for plotting a single-band (grey scale) image.
        Applies to raster, SAR, DEM, and vector cubes, and to SOM maps.
    red (str): Band assigned to the red channel of an RGB composite
        (raster, SAR, and vector cubes).
    green (str): Band assigned to the green channel of an RGB composite.
    blue (str): Band assigned to the blue channel of an RGB composite.
    tile (str): Tile to be plotted (data cubes, probability, uncertainty,
        and variance cubes).
    dates (list[str]): Dates to be plotted (raster, SAR, and vector
        cubes).
    roi (dict | geopandas.GeoDataFrame): Spatial extent (region of
        interest) to plot, in WGS 84.
    labels (list[str]): Labels to plot (probability and variance cubes).
    bands (list[str]): Bands to be viewed (patterns and time series
        predictions).
    legend (dict): Associates labels to colors, or a legend specification
        for SOM plots.
    legend_position (str): Where to place the legend (typically "inside"
        or "outside", with defaults varying by plot type).
    legend_title (str): Title of the legend (probability and variance
        cubes).
    palette (str): An RColorBrewer or "cols4all" (or HCL) palette used
        for color mapping.
    rev (bool): Whether to reverse the color order in the palette.
    scale (float): Relative scale of plot text and map (typically 0.4 to
        1.0).
    quantile (float): Minimum quantile to plot (probability and variance
        cubes).
    first_quantile (float): First quantile for stretching images.
    last_quantile (float): Last quantile for stretching images.
    max_cog_size (int): Maximum size of COG (Cloud Optimized GeoTIFF)
        overviews, in lines/columns or pixels.
    seg_color (str): Color used to draw segment boundaries (vector cubes).
    line_width (float): Line width used to draw segment boundaries
        (vector cubes).
    type (str): Type of plot; meaning depends on the object. For accuracy
        objects it is "confusion_matrix" or "metrics"; for variance cubes
        it is "map" or "hist"; for SOM maps it is "codes" or "mapping".
    cluster: Cluster object produced by `sits_cluster_dendro`, used when
        plotting a dendrogram.
    cutree_height (float): Height at which to draw a dashed horizontal
        line indicating where the dendrogram is cut.
    name_cluster (str): Cluster to plot (SOM cluster evaluation).
    title (str): Title of the plot (SOM cluster evaluation).
    year_grid (bool): Whether to plot patterns as a grid of panels with
        labels as columns and years as rows. Defaults to False.
    tree_idx (int): Index of the tree to be plotted for an XGBoost model.
    plot_embedding (str): For embedding predictions, either "none" (plot
        only predicted class intervals) or "area" (overlay a smoothed
        vertical embedding profile per year).
    stretch (tuple[float, float]): For embedding plots, lower/upper
        quantiles used to stretch embedding values before plotting.
    class_alpha (float): Transparency of class polygons in embedding plots
        (0-1).
    area_alpha (float): Transparency of the embedding area in embedding
        plots (0-1).
    area_width (float): Horizontal width fraction of the embedding area.
    area_spar (float): Smoothing parameter for the embedding area spline.
    **kwargs (dict): Further specifications passed to the underlying plot.

Returns:
    None: A plot is produced. Depending on the input type this may be a
    color map of classified pixels, an RGB or grey-scale image, a
    probability or uncertainty map, a variance map (optionally with
    segment overlays), a dendrogram, a confusion matrix, a SOM map, a
    model diagnostic plot, or a plot for patterns, predictions,
    embeddings, and t-SNE projections. Some methods are called only for
    their side effect of drawing the plot.

Notes:
    The `roi` argument can be defined as a `dict` giving the spatial
    extent (for example with `lon_min`, `lon_max`, `lat_min`, `lat_max`),
    a `geopandas.GeoDataFrame`, or another spatial specification accepted
    by `sits`. Vector cube plots overlay the segments produced by
    `sits_segment` on top of the raster image; their appearance is
    controlled by `seg_color` and `line_width`.

Examples:
    from pysits import *

    # Plot a set of time series patterns
    patterns = sits_patterns(cerrado_2classes)
    plot(patterns)

    # Train a random forest model and plot variable importance
    rfor_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor())
    plot(rfor_model)

    # Plot a SOM map produced from a set of samples
    som_map = sits_som_map(samples_modis_ndvi)
    plot(som_map)
