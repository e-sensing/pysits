Train a model using Lightweight Temporal Self-Attention Encoder

Implementation of Light Temporal Attention Encoder (L-TAE) for satellite image
time series. This is a lightweight version of the temporal attention encoder
proposed by Garnot et al. For the TAE, please see `sits_tae`.
TAE is a simplified version of the well-known self-attention architecture which
is used in large language models. Its modified self-attention scheme that uses
the input embeddings as values. TAE defines a single master query for each
sequence, computed from the temporal average of the queries. This master query
is compared to the sequence of keys to produce a single attention mask used to
weight the temporal mean of values into a single feature vector.
The lightweight version of TAE further simplifies the TAE model. It defines
master query of each head as a model parameter instead of the results of a
linear layer, as is done it TAE. The authors argue that such simplification
reduces the number of parameters, while the lack of flexibility is compensated
by the larger number of available heads.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    samples_validation (SITSTimeSeriesModel): Time series with the
        validation samples. If `samples_validation` parameter is provided,
        `validation_split` is ignored.
    epochs (int): Number of iterations to train the model (min = 1, max =
        20000).
    batch_size (int): Number of samples per gradient update (min = 16, max
        = 2048).
    validation_split (float): Fraction of training data to be used as
        validation data.
    optimizer: Optimizer function to be used.
    opt_hparams (dict): Hyperparameters for optimizer: `lr` : Learning rate
        of the optimizer `eps`: Term added to the denominator to improve
        numerical stability. `weight_decay`: L2 regularization rate.
    lr_decay_epochs (int): Number of epochs to reduce learning rate.
    lr_decay_rate (float): Decay factor for reducing learning rate.
    patience (int): Number of epochs without improvements until training
        stops.
    min_delta (float): Minimum improvement in loss function to reset the
        patience counter.
    seed (int): Seed for random values.
    verbose (bool): Verbosity mode. Default is `False`.

Returns:
    R: A fitted model to be used for classification of data cubes.

Notes:
    `sits` provides a set of default values for all classification models.
    These settings have been chosen based on testing by the authors.
    Nevertheless, users can control all parameters for each model. Novice users
    can rely on the default values, while experienced ones can fine-tune deep
    learning models using `sits_tuning`.
    This function is based on the paper by Vivien Garnot referenced below and
    code available on github at https://github.com/VSainteuf/lightweight-
    temporal-attention-pytorch If you use this method, please cite the original
    TAE and the LTAE paper.
    We also used the code made available by Maja Schneider in her work with
    Marco Körner referenced below and available at
    https://github.com/maja601/RC2020-psetae.

Examples:
    from pysits import *
    import tempfile

    # create a lightTAE model
    torch_model = sits_train(samples_modis_ndvi, sits_lighttae())
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
        data=cube, ml_model=torch_model, output_dir=tempfile.mkdtemp()
    )
    # plot the probability cube
    plot(probs_cube)
    # smooth the probability cube using Bayesian statistics
    bayes_cube = sits_smooth(probs_cube, output_dir=tempfile.mkdtemp())
    # plot the smoothed cube
    plot(bayes_cube)
    # label the probability cube
    label_cube = sits_label_classification(
        bayes_cube,
        output_dir=tempfile.mkdtemp()
    )
    # plot the labelled cube
    plot(label_cube)
