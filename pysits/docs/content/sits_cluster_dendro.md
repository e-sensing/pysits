Find clusters in time series samples

These functions support hierarchical agglomerative clustering in sits. They
provide support from creating a dendrogram and using it for cleaning samples.
`sits_cluster_dendro()` takes a set of time series and produces the same
data with an added "cluster" column. The function first calculates a
dendrogram and obtains a validity index for best clustering using the adjusted
Rand Index. After cutting the dendrogram using the chosen validity index, it
assigns a cluster to each sample.
`sits_cluster_frequency()` computes the contingency table between labels and
clusters and produces a matrix. Its input is produced by
`sits_cluster_dendro()`.
`sits_cluster_clean()` takes time series data that has an additional
`cluster` column produced by `sits_cluster_dendro()` and removes labels that
are minority in each cluster.

Args:
    samples (SITSTimeSeriesModel): input set of time series.
    bands (list[str]): bands to be used in the clustering.
    dist_method (str): one of the supported distances "dtw": DTW with a
        Sakoe-Chiba constraint. "dtw2": DTW with L2 norm and Sakoe-Chiba
        constraint. "dtw_basic": A faster DTW with less functionality.
        "lbk": Keogh's lower bound for DTW. "lbi": Lemire's lower bound for
        DTW.
    linkage (str): agglomeration method to be used. One of "ward.D",
        "ward.D2", "single", "complete", "average", "mcquitty", "median"
        or "centroid".
    k (int): desired number of clusters (overrides default value).
    palette (str): color palette as per `grDevices::hcl.pals()` function.
    **kwargs (dict): additional parameters to be passed to
        dtwclust::tsclust() function.

Returns:
    SITSTimeSeriesModel: time series with a "cluster" column.

Notes:
    Please refer to the sits documentation available in
    https://e-sensing.github.io/sitsbook/ for detailed examples.

Examples:
    from pysits import *

    # default
    clusters = sits_cluster_dendro(cerrado_2classes)
    # with parameters
    clusters = sits_cluster_dendro(cerrado_2classes,
        bands="NDVI", k=5
    )
