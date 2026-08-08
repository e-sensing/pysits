Train a model using Temporal Self-Attention Encoder

Implementation of Temporal Attention Encoder (TAE) for satellite image time
series classification.
TAE is a simplified version of the well-known self-attention architecture used
in large language models. Its modified self-attention scheme that uses the
input embeddings as values. TAE defines a single master query for each
sequence, computed from the temporal average of the queries. This master query
is compared to the sequence of keys to produce a single attention mask used to
weight the temporal mean of values into a single feature vector.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    samples_validation (SITSTimeSeriesModel): Time series with the
        validation samples. If the `samples_validation` parameter is
        provided, the `validation_split` parameter is ignored.
    epochs (int): Number of iterations to train the model.
    batch_size (int): Number of samples per gradient update.
    validation_split (float): Number between 0 and 1. Fraction of training
        data to be used as validation data.
    optimizer: Optimizer function to be used.
    opt_hparams (dict): Hyperparameters for optimizer: lr : Learning rate of
        the optimizer eps: Term added to the denominator to improve
        numerical stability. weight_decay: L2 regularization
    lr_decay_epochs (int): Number of epochs to reduce learning rate.
    lr_decay_rate (float): Decay factor for reducing learning rate.
    patience (int): Number of epochs without improvements until training
        stops.
    min_delta (float): Minimum improvement to reset the patience counter.
    seed (int): Seed for random values.
    verbose (bool): Verbosity mode. Default is False.

Returns:
    SITSMachineLearningMethod: A fitted model to be used for classification.

Notes:
    `sits` provides a set of default values for all classification models.
    These settings have been chosen based on testing by the authors.
    Nevertheless, users can control all parameters for each model. Novice users
    can rely on the default values, while experienced ones can fine-tune deep
    learning models using `sits_tuning`.
    This function is based on the paper by Vivien Garnot referenced below and
    code available on github at https://github.com/VSainteuf/pytorch-psetae.
    We also used the code made available by Maja Schneider in her work with
    Marco K\n    https://github.com/maja601/RC2020-psetae.
    If you use this method, please cite Garnot's and Schneider's work.

Examples:
    from pysits import *
    import tempfile

    # create a TAE model
    torch_model = sits_train(samples_modis_ndvi, sits_tae())
    # plot the model
    plot(torch_model)
    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # classify a data cube
    probs_cube = sits_classify(
        data=cube, ml_model=torch_model, output_dir=tempfile.gettempdir()
    )
    # plot the probability cube
    plot(probs_cube)
    # smooth the probability cube using Bayesian statistics
    bayes_cube = sits_smooth(probs_cube, output_dir=tempfile.gettempdir())
    # plot the smoothed cube
    plot(bayes_cube)
    # label the probability cube
    label_cube = sits_label_classification(
        bayes_cube,
        output_dir=tempfile.gettempdir()
    )
    # plot the labelled cube
    plot(label_cube)
