Show label frequency in each cluster produced by dendrogram analysis

Show label frequency in each cluster produced by dendrogram analysis

Args:
    samples (SITSTimeSeriesModel): input set of time series with
        additional cluster information produced by
        `sits_cluster_dendro()`.

Returns:
    SITSTable: frequencies of labels in clusters.

Examples:
    from pysits import *

    clusters = sits_cluster_dendro(cerrado_2classes)
    freq = sits_cluster_frequency(clusters)
    print(freq)
