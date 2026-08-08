Train a Long Short Term Memory Fully Convolutional Network

Uses a branched neural network consisting of a lstm (long short term memory)
branch and a three-layer fully convolutional branch (FCN) followed by
concatenation to classify time series data.
This function is based on the paper by Fazle Karim, Somshubra Majumdar, and
Houshang Darabi. If you use this method, please cite the original LSTM with FCN
paper.
The original python code is available at the website
https://github.com/titu1994/LSTM-FCN. This code is licensed as GPL-3.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    samples_validation (SITSTimeSeriesModel): Time series with the
        validation samples. If the `samples_validation` parameter is
        provided, the `validation_split` parameter is ignored.
    cnn_layers (list[int]): Number of 1D convolutional filters per layer.
    cnn_kernels (list[int]): Size of the 1D convolutional kernels.
    lstm_width (int): Number of neurons in the lstm hidden layer.
    lstm_dropout (float): Dropout rate of the lstm layer.
    epochs (int): Number of iterations to train the model.
    batch_size (int): Number of samples per gradient update.
    validation_split (float): Fraction of training data to be used for
        validation.
    optimizer: Optimizer function to be used.
    opt_hparams (dict): Hyperparameters for optimizer: lr : Learning rate
        of the optimizer eps: Term added to the denominator to improve
        numerical stability. weight_decay: L2 regularization.
    lr_decay_epochs (int): Number of epochs to reduce learning rate.
    lr_decay_rate (float): Decay factor for reducing learning rate.
    patience (int): Number of epochs without improvements until training
        stops.
    min_delta (float): Minimum improvement in loss function to reset the
        patience counter.
    seed (int): Seed for random values.
    verbose (bool): Verbosity mode. Default is `False`.

Returns:
    SITSMachineLearningMethod: A fitted model to be used for
        classification.

Examples:
    from pysits import *
    import tempfile

    # create an LSTM model
    torch_model = sits_train(
        samples_modis_ndvi,
        sits_lstm_fcn(epochs=20, verbose=True)
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
