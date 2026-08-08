View data cubes and samples in leaflet

Uses leaflet to visualize time series, raster cube and classified images.

Args:
    x (SITSTimeSeriesModel | SITSCubeModel | pandas.DataFrame): time
        series samples, SOM map, raster cube, probability cube, vector
        cube, or classified cube.
    legend (dict): associates labels to colors.
    palette (str): color palette from RColorBrewer.
    radius (float): radius of circle markers.
    add (bool): add image to current leaflet.
    id_neurons (list[int]): neurons from the SOM map to be shown.
    band (str): single band for viewing false color images.
    red (str): band for red color.
    green (str): band for green color.
    blue (str): band for blue color.
    tiles (list[str]): tiles to be plotted (in case of a multi-tile
        cube).
    dates (list[str]): dates to be plotted.
    rev (bool): revert color palette?
    opacity (float): opacity of segment fill or class cube.
    max_cog_size (int): maximum size of COG overviews (lines or
        columns).
    first_quantile (float): first quantile for stretching images.
    last_quantile (float): last quantile for stretching images.
    leaflet_megabytes (float): maximum size for leaflet (in MB).
    version (str): version name (to compare different classifications).
    labels (list[str]): labels to be plotted (in case of probs and
        variance cubes).
    seg_color (str): color for segment boundaries.
    line_width (float): line width for segments (in pixels).
    **kwargs (dict): further specifications for sits_view.

Returns:
    None: a leaflet object containing either samples or data cubes
        embedded in a global map that can be visualized directly in a
        viewer.

Notes:
    To show a false color image, use "band" to chose one of the bands, "tiles"
    to select tiles, "first_quantile" and "last_quantile" to set the cutoff
    points. Choose only one date in the "dates" parameter. The color scheme is
    defined by either "palette" (use an available color scheme) or legend
    (user-defined color scheme). To see which palettes are pre-defined, use
    `cols4all::g4a_gui` or select any ColorBrewer name. The "rev" parameter
    reverts the order of colors in the palette.
    To show an RGB composite, select "red", "green" and "blue" bands, "tiles",
    "dates", "opacity", "first_quantile" and "last_quantile". One can also get
    an RGB composite, by selecting one band and three dates. In this case, the
    first date will be shown in red, the second in green and third in blue.
    Probability cubes are shown in false color. The parameter "labels" controls
    which labels are shown. If left blank, only the first map is shown. For
    color control, use "palette", "legend", and "rev" (as described above).
    Vector cubes have both a vector and a raster component. The vector part are
    the segments produced by `sits_segment`. Their visual output is controlled
    by "seg_color" and "line_width" parameters. The raster output works in the
    same way as the false color and RGB views described above.
    Classified cubes need information on how to render each class. There are
    three options: (a) the classes are part of an existing color scheme; (b)
    the user provides a legend which associates each class to a color; (c) use
    a generic palette (such as "Spectral") and allocate colors based on this
    palette. To find out how to create a customized color scheme, read the
    chapter "Data Visualisation in sits" in the sits book.
    To compare different classifications, use the "version" parameter to
    distinguish between the different maps that are shown.
    Vector classified cubes are displayed as classified cubes, with the
    segments overlaid on top of the class map, controlled by "seg_color" and
    "line_width".
    Samples are shown on the map based on their geographical locations and on
    the color of their classes assigned in their color scheme. Users can also
    assign a legend or a palette to choose colors. See information above on the
    display of classified cubes.
    For all types of data cubes, the following parameters apply:
    - opacity: controls the transparency of the map.
    - max_cog_size: For COG data, controls the level of aggregation to be used
      for display, measured in pixels, e.g., a value of 512 will select a 512 x
      512 aggregated image. Small values are faster to show, at a loss of
      visual quality.
    - leaflet_megabytes: maximum size of leaflet to be shown associated to the
      map (in megabytes). Bigger values use more memory.
    - add: controls whether a new visualisation will be overlaid on top of an
      existing one. Default is False.

Examples:
    from pysits import *
    import tempfile

    # view samples
    sits_view(cerrado_2classes)

    # create a local data cube
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    modis_cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # view the data cube
    sits_view(modis_cube, band="NDVI")

    # train a model
    rf_model = sits_train(samples_modis_ndvi, sits_rfor())

    # classify the cube
    modis_probs = sits_classify(
        data=modis_cube,
        ml_model=rf_model,
        output_dir=tempfile.gettempdir()
    )

    # generate a map
    modis_label = sits_label_classification(
        modis_probs,
        output_dir=tempfile.gettempdir()
    )

    # view the classified map
    sits_view(modis_label)

    # add the NDVI band for the first date
    sits_view(modis_cube,
        band="NDVI",
        class_cube=modis_label,
        dates=sits_timeline(modis_cube)[0],
        add=True
    )

    # view the classified map with the RGB image
    sits_view(modis_cube,
        red="NDVI", green="NDVI", blue="NDVI",
        class_cube=modis_label,
        dates=sits_timeline(modis_cube)[0],
        add=True
    )

    # create an uncertainty cube
    modis_uncert = sits_uncertainty(
        cube=modis_probs,
        output_dir=tempfile.gettempdir()
    )

    # view the uncertainty cube
    sits_view(modis_uncert, rev=True, add=True)
