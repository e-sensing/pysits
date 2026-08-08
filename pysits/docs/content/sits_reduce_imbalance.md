Reduce imbalance in a set of samples

Takes a set of samples with different labels and returns a new set. Deals
with class imbalance using the synthetic minority oversampling technique
(SMOTE) for oversampling. Undersampling is done using the SOM methods
available in the `sits` package.

Args:
    samples (SITSTimeSeriesModel): Sample set to rebalance.
    n_samples_over (int): Number of samples to oversample for classes with
        samples less than this number.
    n_samples_under (int): Number of samples to undersample for classes
        with samples more than this number.
    method (str): Method for oversampling (default = "smote").
    multicores (int): Number of cores to process the data (default 2).

Returns:
    SITSTimeSeriesModel: A set of samples with reduced imbalance.

Notes:
    Many training samples for Earth observation data analysis are
    imbalanced. This situation arises when the distribution of samples
    associated with each label is uneven. Sample imbalance is an
    undesirable property of a training set. Reducing sample imbalance
    improves classification accuracy.
    The function `sits_reduce_imbalance` increases the number of samples of
    least frequent labels, and reduces the number of samples of most
    frequent labels. To generate new samples, `sits` uses the SMOTE method
    that estimates new samples by considering the cluster formed by the
    nearest neighbors of each minority label.
    To perform undersampling, `sits_reduce_imbalance`) builds a SOM map for
    each majority label based on the required number of samples. Each
    dimension of the SOM is set to ceiling(sqrt(new_number_samples/4)) to
    allow a reasonable number of neurons to group similar samples. After
    calculating the SOM map, the algorithm extracts four samples per neuron
    to generate a reduced set of samples that approximates the variation of
    the original one. See also `sits_som_map`.

Examples:
    from pysits import *

    # print the labels summary for a sample set
    summary(samples_modis_ndvi)
    # reduce the sample imbalance
    new_samples = sits_reduce_imbalance(samples_modis_ndvi,
        n_samples_over=200,
        n_samples_under=200,
        multicores=1
    )
    # print the labels summary for the rebalanced set
    summary(new_samples)
