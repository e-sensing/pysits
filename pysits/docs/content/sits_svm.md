Train support vector machine models

This function receives a set of training samples with a set of
attributes X for each observation Y. These attributes are the values of
the time series for each band. The SVM algorithm is used for
multiclass-classification. For this purpose, it uses the
"one-against-one" approach, in which k(k-1)/2 binary classifiers are
trained; the appropriate class is found by a voting scheme. This
function is a front-end to the "svm" method in the "e1071" package.
Please refer to the documentation in that package for more details.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    formula (SITSMachineLearningMethod): Symbolic description of the
        model to be fit (default: sits_formula_linear).
    scale (bool): Indicates whether the variables should be scaled.
    cachesize (int): Cache memory in MB (default = 1000).
    kernel (str): Kernel used in training and predicting. Options:
        "linear", "polynomial", "radial", "sigmoid" (default:
        "radial").
    degree (int): Exponential of polynomial type kernel (default: 3).
    coef0 (float): Parameter needed for kernels of type polynomial and
        sigmoid (default: 0).
    cost (float): Cost of constraints violation (default: 10).
    tolerance (float): Tolerance of termination criterion (default:
        0.001).
    epsilon (float): Epsilon in the insensitive-loss function (default:
        0.1).
    cross (int): Number of cross validation folds applied to assess the
        quality of the model (default: 10).
    **kwargs (dict): Other parameters to be passed to e1071::svm
        function.

Returns:
    SITSMachineLearningMethod: Model fitted to input data (to be passed
        to `sits_classify`).

Notes:
    Please refer to the sits documentation available in
    https://e-sensing.github.io/sitsbook/ for detailed examples.

Examples:
    from pysits import *

    # Example of training a model for time series classification
    # Retrieve the samples for Mato Grosso
    # train an SVM model
    ml_model = sits_train(samples_modis_ndvi, ml_method=sits_svm)
    # classify the point
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    # classify the point
    point_class = sits_classify(data=point_ndvi, ml_model=ml_model)
    plot(point_class)
