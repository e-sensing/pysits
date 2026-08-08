Cross-validate time series samples

Splits the set of time series into training and validation and perform k-fold
cross-validation.

Args:
    samples (SITSTimeSeriesModel): Time series.
    folds (int): Number of partitions to create.
    ml_method (SITSMachineLearningMethod): Machine learning method.
    impute_fn: Imputation function to remove NA.
    multicores (int): Number of cores to process in parallel.
    gpu_memory (int): Memory available in GPU in GB (default = 4)
    batch_size (int): Batch size for GPU classification.
    progress (bool): Show progress bar?

Returns:
    resolve_and_invoke_accuracy_class: A confusion matrix to be used for
        validation assessment.

Notes:
    Cross-validation is a technique for assessing how the results of a
    statistical analysis will generalize to an independent data set. It is
    mainly used in settings where the goal is prediction, and one wants to
    estimate how accurately a predictive model will perform. One round of
    cross-validation involves partitioning a sample of data into complementary
    subsets, performing the analysis on one subset (called the training set),
    and validating the analysis on the other subset (called the validation set
    or testing set).
    The k-fold cross validation method involves splitting the dataset into
    k-subsets. For each subset is held out while the model is trained on all
    other subsets. This process is completed until accuracy is determine for
    each instance in the dataset, and an overall accuracy estimate is provided.
    This function returns the confusion matrix, and Kappa values.

Examples:
    from pysits import *
    import tempfile
    import os

    # A dataset containing a tibble with time series samples
    # for the Mato Grosso state in Brasil
    # create a list to store the results
    results = []
    # accuracy assessment lightTAE
    acc_rfor = sits_kfold_validate(
        samples_modis_ndvi,
        folds=5,
        ml_method=sits_rfor()
    )
    # use a name
    acc_rfor.name = "Rfor"
    # put the result in a list
    results.append(acc_rfor)
    # save to xlsx file
    output_file = os.path.join(tempfile.gettempdir(), "accuracy_mato_grosso_dl_.xlsx")
    sits_to_xlsx(
        results,
        file=output_file
    )
