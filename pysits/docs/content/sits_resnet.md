Train ResNet classification models

Use a ResNet architecture for classifying image time series. The ResNet (or
deep residual network) was proposed by a team in Microsoft Research for 2D
image classification. ResNet tries to address the degradation of accuracy in a
deep network. The idea is to replace a deep network with a combination of
shallow ones. In the paper by Fawaz et al. (2019), ResNet was considered the
best method for time series classification, using the UCR dataset. Please refer
to the paper for more details.
The R-torch version is based on the code made available by Zhiguang Wang,
author of the original paper. The code was developed in python using keras.
https://github.com/cauchyturing (repo:
UCR_Time_Series_Classification_Deep_Learning_Baseline)
The R-torch version also considered the code by Ignacio Oguiza, whose
implementation is available at
https://github.com/timeseriesAI/tsai/blob/main/tsai/models/ResNet.py.
There are differences between Wang's Keras code and Oguiza torch code. In this
case, we have used Wang's keras code as the main reference.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    samples_validation (SITSTimeSeriesModel): Time series with the
        validation samples. If provided, `validation_split` is ignored.
    blocks (list[int]): Number of 1D convolutional filters for each block
        of three layers.
    kernels (list[int]): Size of the 1D convolutional kernels.
    epochs (int): Number of iterations to train the model, for each layer
        of each block.
    batch_size (int): Number of samples per gradient update.
    validation_split (float): Fraction of training data to be used as
        validation data.
    optimizer: Optimizer function to be used.
    opt_hparams (dict): Hyperparameters for optimizer: lr : Learning rate
        of the optimizer eps: Term added to the denominator to improve
        numerical stability. weight_decay: L2 regularization
    lr_decay_epochs (int): Number of epochs to reduce learning rate.
    lr_decay_rate (float): Decay factor for reducing learning rate.
    patience (int): Number of epochs without improvements until training
        stops.
    min_delta (float): Minimum improvement in loss function to reset the
        patience counter.
    seed (int): Seed for random values.
    verbose (bool): Verbosity mode. Default is `False`.

Returns:
    SITSMachineLearningMethod: A fitted model to be used for classification.

Examples:
    from pysits import *
    import tempfile

    # create a ResNet model
    torch_model = sits_train(samples_modis_ndvi, sits_resnet())
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
