Train temporal convolutional neural network models

Use a TempCNN algorithm to classify data, which has two stages: a 1D CNN and a
multi-layer perceptron. Users can define the depth of the 1D network, as well
as the number of perceptron layers.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    samples_validation (SITSTimeSeriesModel): Time series with the validation
        samples. If provided, the `validation_split` parameter is ignored.
    cnn_layers (list[int]): Number of 1D convolutional filters per layer.
    cnn_kernels (list[int]): Size of the 1D convolutional kernels.
    cnn_dropout_rates (list[float]): Dropout rates for 1D convolutional
        filters.
    dense_layer_nodes (int): Number of nodes in the dense layer.
    dense_layer_dropout_rate (float): Dropout rate (0,1) for the dense layer.
    epochs (int): Number of iterations to train the model.
    batch_size (int): Number of samples per gradient update.
    validation_split (float): Fraction of training data to be used for
        validation.
    optimizer: Optimizer function to be used.
    opt_hparams (dict): Hyperparameters for optimizer: lr : Learning rate of
        the optimizer eps: Term added to the denominator to improve numerical
        stability. weight_decay: L2 regularization
    lr_decay_epochs (int): Number of epochs to reduce learning rate.
    lr_decay_rate (float): Decay factor for reducing learning rate.
    patience (int): Number of epochs without improvements until training stops.
    min_delta (float): Minimum improvement in loss function to reset the
        patience counter.
    seed (int): Seed for random values.
    verbose (bool): Verbosity mode. Default is `False`.

Returns:
    R: A fitted model to be used for classification.

Notes:
    `sits` provides a set of default values for all classification models.
    These settings have been chosen based on testing by the authors.
    Nevertheless, users can control all parameters for each model. Novice users
    can rely on the default values, while experienced ones can fine-tune deep
    learning models using `sits_tuning`.
    This function is based on the paper by Charlotte Pelletier referenced
    below. If you use this method, please cite the original tempCNN paper.
    The torch version is based on the code made available by the BreizhCrops
    team: Marc Russwurm, Charlotte Pelletier, Marco Korner, Maximilian Zollner.
    The original python code is available at the website
    https://github.com/dl4sits/BreizhCrops. This code is licensed as GPL-3.

Examples:
    from pysits import *
    import tempfile

    # create a TempCNN model
    torch_model = sits_train(
        samples_modis_ndvi,
        sits_tempcnn(epochs=20, verbose=True)
    )
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
