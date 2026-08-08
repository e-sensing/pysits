Cleans the samples based on SOM map information

`sits_som_clean_samples()` evaluates the quality of the samples based on the
results of the SOM map.

Args:
    som_map: returned by `sits_som_map`.
    prior_threshold (float): threshold of conditional probability (frequency
        of samples assigned to the same SOM neuron).
    posterior_threshold (float): threshold of posterior probability
        (influenced by the SOM neighborhood).
    keep (list[str]): which types of evaluation to be maintained in the data.

Returns:
    SITSTimeSeriesModel: samples with two additional columns. The first
        indicates if each sample is clean, should be analyzed or should be
        removed. The second is the posterior probability of the sample. The
        "keep" parameter indicates which.

Notes:
    The algorithm identifies noisy samples, using `prior_threshold` for the
    prior probability and `posterior_threshold` for the posterior probability.
    Each sample receives an evaluation tag, according to the following rule:
    (a) If the prior probability is < `prior_threshold`, the sample is tagged
    as "remove"; (b) If the prior probability is >= `prior_threshold` and the
    posterior probability is >=`posterior_threshold`, the sample is tagged as
    "clean"; (c) If the prior probability is >= `posterior_threshold` and the
    posterior probability is < `posterior_threshold`, the sample is tagged as
    "analyze" for further inspection. The user can define which tagged samples
    will be returned using the "keep" parameter, with the following options:
    "clean", "analyze", "remove".

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
