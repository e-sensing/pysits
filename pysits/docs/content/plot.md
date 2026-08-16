Plot sits objects.

A single dispatching function that produces a plot appropriate to the type
of the object passed as `x`. It covers data cubes (raster, SAR, DEM,
vector), probability and uncertainty products, variance cubes, patterns,
time-series predictions, embeddings, clustering and SOM outputs, accuracy
tables, and trained models. Depending on the object type, the plot is
rendered as a map, a chart, or a raster image.

The accepted keyword arguments depend on the type of `x`. The sections
below group the parameters by the kind of object being plotted.

Args:
    x (SITSCubeModel | SITSTimeSeriesModel | SITSTimeSeriesPatternsModel | SITSMachineLearningMethod | SITSConfusionMatrix):
        Object to be plotted. Supported kinds include raster, SAR, DEM,
        and vector cubes; classified, probability, uncertainty, and
        variance cubes; patterns; time-series and embedding predictions;
        geographic distances; clustering and SOM outputs; accuracy
        tables; t-SNE projections; and trained models.
    y: Ignored. Present for compatibility with the generic `plot`.
    band (str): For raster, SAR, DEM, and vector cubes, the band used to
        plot a grey (B/W) image. For SOM maps, the band to be plotted.
    red (str): Band assigned to the red channel for RGB plots of raster,
        SAR, and vector cubes.
    green (str): Band assigned to the green channel for RGB plots.
    blue (str): Band assigned to the blue channel for RGB plots.
    tile (str): Tile to be plotted (for cube objects).
    dates (list[str]): Dates to be plotted (raster, SAR, and vector
        cubes).
    roi (dict): Spatial extent (region of interest) to plot, in WGS 84.
        See notes.
    labels (list[str]): Labels to plot (probability, variance, and vector
        cubes).
    bands (list[str]): Bands to be viewed (for patterns and time-series
        predictions).
    legend (dict): Maps labels to colors (class cubes, SOM maps, and
        cluster confusion plots).
    legend_position (str): Where to place the legend. Typical default is
        `"inside"` for RGB/grey plots and `"outside"` for classified and
        probability maps.
    legend_title (str): Title of the legend for probability and variance
        cubes (for example `"probs"` or `"logvar"`).
    palette (str): An `RColorBrewer` or `cols4all` palette. For
        chart-based plots (predictions, embeddings, clusters, t-SNE), an
        HCL palette name.
    rev (bool): Whether to reverse the color order in the palette.
    scale (float): Relative scale (roughly 0.4 to 1.0) of the plot text
        and map.
    quantile (float): Minimum quantile to plot (probability and variance
        cubes).
    first_quantile (float): First quantile used for stretching images.
    last_quantile (float): Last quantile used for stretching images.
    max_cog_size (int): Maximum size of COG (Cloud Optimized GeoTIFF)
        overviews, in lines/columns (pixels).
    seg_color (str): Color used for segment borders in vector cubes.
    line_width (float): Line width used for segment borders in vector
        cubes.
    type (str): Type of plot. For accuracy objects, either
        `"confusion_matrix"` or `"metrics"`. For variance cubes, `"map"`
        or `"hist"`. For SOM maps, `"codes"` (neuron weight time series)
        or `"mapping"` (number of samples per neuron).
    year_grid (bool): For patterns, whether to plot a grid of panels
        using labels as columns and years as rows (default `False`).
    cluster: For clustering plots, the cluster object produced by
        `sits_cluster_dendro`.
    cutree_height (float): For clustering plots, the height at which to
        draw a dashed horizontal line indicating where the dendrogram is
        cut.
    name_cluster (str): For SOM cluster evaluation, the cluster to plot.
    title (str): For SOM cluster evaluation, the title of the plot.
    tree_idx (int): For XGBoost models, the index of the tree to be
        plotted.
    plot_embedding (str): For embedding predictions, either `"none"` (plot
        only the predicted class intervals) or `"area"` (overlay a
        smoothed vertical embedding profile per year).
    stretch (list[float]): For embedding predictions, the lower and upper
        quantiles used to stretch embedding values before plotting
        (default `[0.02, 0.98]`).
    class_alpha (float): For embedding predictions, transparency of the
        class polygons in `[0, 1]` (default `0.7`).
    area_alpha (float): For embedding predictions, transparency of the
        embedding area in `[0, 1]` (default `0.25`).
    area_width (float): For embedding predictions, the horizontal width
        fraction of the embedding area along the time axis.
    area_spar (float): For embedding predictions, the smoothing parameter
        passed to the spline fit (default `0.6`); higher values produce
        smoother profiles.
    image_args (dict): Geometry to render the figure with, with any of the
        keys `width` and `height` (in inches), and `res` (in dots per
        inch). See the notes on figure size below.
    **kwargs (dict): Further specifications for the plot. The keywords
        understood depend on the type of `x` (see below).

Returns:
    SITSPlot | SITSPlotList: The rendered figure. Objects that produce
        several figures, samples with more than one band or label, for
        example, return a `SITSPlotList`, which behaves as a sequence of
        `SITSPlot`.

        Maps of cubes yield color or B/W raster images (optionally
        overlaid with segment boundaries for vector cubes). Probability,
        uncertainty, and variance cubes yield per-class or per-pixel maps.
        Classified cubes yield color maps where each pixel is colored by
        its label. Chart-based plots (patterns, predictions, embeddings,
        clusters, t-SNE, model diagnostics) render the corresponding plot.

        How the figure reaches the page depends on where the code runs.
        In a notebook, or a Quarto document using the `jupyter` engine,
        the returned figure is rendered as the result of the cell. In
        RStudio, or a Quarto document using the `knitr` engine, the
        figures are handed to `knitr` as it renders the chunk, so each
        one becomes a document figure of its own, with its own caption,
        cross-reference, and layout. Everywhere else plotting displays
        nothing by itself: use `save` to write the figure to a file, or
        `show` to open it in an image viewer.

Notes:
        The set of valid keyword arguments depends on the type of `x`;
        passing arguments that do not apply to a given object type has no
        effect. When a region of interest (`roi`) is supported, it defines
        the spatial extent to plot in WGS 84.

Examples:
    from pysits import *

    # Plot a set of time-series patterns (one average pattern per label)
    patterns = sits_patterns(samples_modis_ndvi)
    plot(patterns)

    # Train a random forest model and plot its important variables
    rf_model = sits_train(samples_modis_ndvi, ml_method=sits_rfor())
    plot(rf_model)

    # Render a larger figure, and write it to a file
    figure = plot(rf_model, image_args={"width": 12, "height": 8})
    figure.save("model.png")

    # Set the size of every figure that follows
    set_plot_options(width=8, height=5, dpi=150)

    # Objects with several bands or labels produce one figure each
    figures = plot(samples_l8_rondonia_2bands)
    figures[0].save("first.png")
