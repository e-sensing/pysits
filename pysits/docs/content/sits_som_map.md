Build a SOM for quality analysis of time series samples

These function use self-organized maps to perform quality analysis in satellite
image time series.

Args:
    data (SITSTimeSeriesModel): samples to be clustered.
    grid_xdim (int): X dimension of the SOM grid (default = 25).
    grid_ydim (int): Y dimension of the SOM grid.
    alpha (float): Starting learning rate (decreases according to number
        of iterations).
    rlen (int): Number of iterations to produce the SOM.
    distance (str): The type of similarity measure (distance). The
        following similarity measurements are supported: `"euclidean"`,
        `"dtw"`, and `"cosine"`. The default similarity measure is
        `"dtw"`. For single-timestep samples (e.g. embeddings), all bands
        are treated as one feature vector. `"dtw"` is not applicable and
        falls back to `"euclidean"`, while `"cosine"` compares the angle
        between the full embedding vectors.
    som_radius (float): Radius of SOM neighborhood.
    mode (str): Type of learning algorithm. The following learning
        algorithm are available: `"online"`, `"batch"`, and `"pbatch"`.
        The default learning algorithm is `"online"`.

Returns:
    SITStructureData: a structure with three members: (1) the samples,
    with one additional column indicating to which neuron each sample has
    been mapped; (2) the Kohonen map, used for plotting and cluster
    quality measures; (3) the labelled neurons, where each class of each
    neuron is associated to two values: (a) the prior probability that
    this class belongs to a cluster based on the frequency of samples of
    this class allocated to the neuron; (b) the posterior probability
    that this class belongs to a cluster, using data for the neighbours
    on the SOM map.

Notes:
    `sits_som_map` creates a SOM map, where high-dimensional data is mapped
    into a two dimensional map, keeping the topological relations between data
    patterns. Each sample is assigned to a neuron, and neurons are placed in
    the grid based on similarity.
    `sits_som_evaluate_cluster` analyses the neurons of the SOM map, and builds
    clusters based on them. Each cluster is a neuron or a set of neuron
    categorized with same label. It produces the percentage of mixture of
    classes in each cluster.
    `sits_som_clean_samples` evaluates sample quality based on the results of
    the SOM map. The algorithm identifies noisy samples, using
    `prior_threshold` for the prior probability and `posterior_threshold` for
    the posterior probability. Each sample receives an evaluation tag,
    according to the following rule: (a) If the prior probability is <
    `prior_threshold`, the sample is tagged as "remove"; (b) If the prior
    probability is >= `prior_threshold` and the posterior probability is
    >=`posterior_threshold`, the sample is tagged as "clean"; (c) If the prior
    probability is >= `posterior_threshold` and the posterior probability is <
    `posterior_threshold`, the sample is tagged as "analyze" for further
    inspection.
    The user can define which tagged samples will be returned using the "keep"
    parameter, with the following options: "clean", "analyze", "remove".
    To learn more about the learning algorithms, check the `kohonen::supersom`
    function.
    The `sits` package implements the `"dtw"` (Dynamic Time Warping) similarity
    measure. The `"euclidean"` similarity measurement come from the
    `kohonen::supersom (dist.fcts)` function.

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
