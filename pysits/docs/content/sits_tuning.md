Tuning machine learning models hyper-parameters

This function performs a random search on values of selected hyperparameters,
and produces a `pandas.DataFrame` with the accuracy and kappa values produced
by a validation procedure. The result allows users to select appropriate
hyperparameters for deep learning models.

Args:
    samples (SITSTimeSeriesModel): Time series set to be validated.
    samples_validation (SITSTimeSeriesModel): Time series set used for
        validation.
    validation_split (float): Percent of original time series set to be
        used for validation (if `samples_validation` is `None`).
    ml_method (SITSMachineLearningMethod): Machine learning method.
    params (dict): Hyper parameters to be passed to `ml_method`. User can
        use `uniform`, `choice`, `randint`, `normal`, `lognormal`,
        `loguniform`, and `beta` distribution functions to randomize
        parameters.
    trials (int): Number of random trials to perform the search.
    multicores (int): Number of cores to process in parallel.
    gpu_memory (int): Memory available in GPU in GB (default = 4).
    batch_size (int): Batch size for GPU classification.
    progress (bool): Show progress bar?

Returns:
    SITSTuningResults: All parameters used to train on each trial ordered
        by accuracy.

Notes:
    Machine learning algorithms have hyperparameters that control the
    algorithm's behaviour. This function allows users to test different
    combinations of hyperparameters for a given sample set, thus selecting a
    set of values which fits the training data. The `sits_tuning` function can
    be used with both traditional machine learning methods (e.g., random
    forests) as well as deep learning ones.
    Instead of performing an exhaustive test of all parameter combinations,
    `sits_tuning` selects them randomly. Validation is done using an
    independent set of samples or by a validation split. The function returns
    the best hyper-parameters in a `dict`. Hyper-parameters passed to `params`
    parameter should be passed by calling `sits_tuning_hparams`.
    Deep learning models use stochastic gradient descent (SGD) techniques to
    find optimal solutions. To perform SGD, models use optimization algorithms
    which have hyperparameters that have to be adjusted to achieve best
    performance for each application.
    When using a GPU for deep learning, `gpu_memory` indicates the memory of
    the graphics card which is available for processing. The parameter
    `batch_size` defines the size of the matrix (measured in number of rows)
    which is sent to the GPU for classification. Users can test different
    values of `batch_size` to find out which one best fits their GPU
    architecture.
    It is not possible to have an exact idea of the size of Deep Learning
    models in GPU memory, as the complexity of the model and factors such as
    CUDA Context increase the size of the model in memory. Therefore, we
    recommend that you leave at least 1GB free on the video card to store the
    Deep Learning model that will be used.
    For users of Apple M3 chips or similar with a Neural Engine, be aware that
    these chips share memory between the GPU and the CPU. Tests indicate that
    the `memsize` should be set to half to the total memory and the
    `batch_size` parameter should be a small number (we suggest the value of
    64). Be aware that increasing these parameters may lead to memory
    conflicts.
