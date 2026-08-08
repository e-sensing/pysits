Evaluate cluster

Remove samples from a given class inside a neuron of another class

Args:
    som_map: A SOM map produced by the `sits_som_map()` function.
    som_eval: An evaluation produced by the `sits_som_evaluate_cluster()`
        function.
    class_cluster (str): Dominant class of a set of neurons.
    class_remove (str): Class to be removed from the neurons of
        `class_cluster`.

Returns:
    SITSTimeSeriesModel: A new set of samples with the desired class
        neurons removed.

Examples:
    from pysits import *

    # create a som map
    som_map = sits_som_map(samples_modis_ndvi)
    # evaluate the som map and create clusters
    som_eval = sits_som_evaluate_cluster(som_map)
    # clean the samples
    new_samples = sits_som_remove_samples(
        som_map, som_eval,
        "Pasture", "Cerrado"
    )
