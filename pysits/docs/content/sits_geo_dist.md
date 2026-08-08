Compute the minimum distances among samples and prediction points.

Compute the minimum distances among samples and samples to prediction points,
following the approach proposed by Meyer and Pebesma(2022).

Args:
    samples (SITSTimeSeriesModel): Time series.
    roi (str | pathlib.Path | geopandas.GeoDataFrame): A region of interest
        (ROI), either a file containing a shapefile or a
        `geopandas.GeoDataFrame`.
    n (int): Maximum number of samples to consider.
    crs (str): CRS of the `samples`.

Returns:
    SITSFrame: sample-to-sample and sample-to-prediction distances.

Notes:
    As pointed out by Meyer and Pebesma, many classifications using machine
    learning assume that the reference data are independent and well-
    distributed in space. In practice, many training samples are strongly
    concentrated in some areas, and many large areas have no samples. This
    function compares two distributions:
    1. The distribution of the spatial distances of reference data to their
       nearest neighbor (sample-to-sample.
    2. The distribution of distances from all points of study area to the
       nearest reference data point (sample-to-prediction).

Examples:
    from pysits import *
    import geopandas as gpd

    # read a shapefile for the state of Mato Grosso, Brazil
    mt_shp = r_package_dir("extdata/shapefiles/mato_grosso/mt.shp", package="sits")
    # convert to a geopandas object
    mt_sf = gpd.read_file(mt_shp)
    # calculate sample-to-sample and sample-to-prediction distances
    distances = sits_geo_dist(
        samples=samples_modis_ndvi,
        roi=mt_sf
    )
    # plot sample-to-sample and sample-to-prediction distances
    plot(distances)
