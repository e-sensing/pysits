Removes labels that are minority in each cluster.

Takes a set of time series that has additional `cluster` information
produced by `sits_cluster_dendro()` and removes labels that are minority
in each cluster.

Args:
    samples (SITSTimeSeriesModel): Set of time series with additional
        cluster information produced by `sits_cluster_dendro()`.

Returns:
    SITSTimeSeriesModel: Set of time series.

Examples:
    from pysits import *

    clusters = sits_cluster_dendro(cerrado_2classes)
    freq1 = sits_cluster_frequency(clusters)
    print(freq1)
    clean_clusters = sits_cluster_clean(clusters)
    freq2 = sits_cluster_frequency(clean_clusters)
    print(freq2)
