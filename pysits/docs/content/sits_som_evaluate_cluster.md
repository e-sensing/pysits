Evaluate cluster

`sits_som_evaluate_cluster()` produces a `SITSFrame` with the clusters
found by the SOM map. For each cluster, it provides the percentage of
classes inside it.

Args:
    som_map: A SOM map produced by the `sits_som_map()` function.

Returns:
    SITSFrame: The purity for each cluster.

Examples:
    from pysits import *

    # create a som map
    som_map = sits_som_map(samples_modis_ndvi)
    # plot the som map
    plot(som_map)
    # evaluate the som map and create clusters
    clusters_som = sits_som_evaluate_cluster(som_map)
    # plot the cluster evaluation
    plot(clusters_som)
    # clean the samples
    new_samples = sits_som_clean_samples(som_map)
