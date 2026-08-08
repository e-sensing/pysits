Train classification models

Given a set of time series, returns trained models. Currently,
sits supports the following models:
- support vector machines: `sits_svm`;
- random forests: `sits_rfor`;
- extreme gradient boosting: `sits_xgboost`;
- light gradient boosting: `sits_lightgbm`;
- multi-layer perceptrons: `sits_mlp`;
- temporal CNN: `sits_tempcnn`;
- residual network encoders: `sits_resnet`;
- LSTM with convolutional networks: `sits_lstm_fcn`;
- temporal self-attention encoders: `sits_lighttae` and `sits_tae`.

Args:
    samples (SITSTimeSeriesModel): Time series with the training samples.
    ml_method (SITSMachineLearningMethod): Machine learning method.

Returns:
    SITSMachineLearningMethod: Model fitted to input data to be passed to
        `sits_classify`.

Notes:
    The main `sits` classification workflow has the following steps:
    1. `sits_cube`: selects a ARD image collection from a cloud provider.
    2. `sits_cube_copy`: copies an ARD image collection from a cloud provider
       to a local directory for faster processing.
    3. `sits_regularize`: create a regular data cube from an ARD image
       collection.
    4. `sits_apply`: create new indices by combining bands of a regular data
       cube (optional).
    5. `sits_get_data`: extract time series from a regular data cube based on
       user-provided labelled samples.
    6. `sits_train`: train a machine learning model based on image time series.
    7. `sits_classify`: classify a data cube using a machine learning model and
       obtain a probability cube.
    8. `sits_smooth`: post-process a probability cube using a spatial smoother
       to remove outliers and increase spatial consistency.
    9. `sits_label_classification`: produce a classified map by selecting the
       label with the highest probability from a smoothed cube.
    `sits_train` provides a standard interface to machine learning models. It
    takes two mandatory parameters: the training data (`samples`) and the ML
    algorithm (`ml_method`). The output is a model that can be used to classify
    individual time series or data cubes with `sits_classify`.
    `sits` provides a set of default values for all classification models.
    These settings have been chosen based on testing by the authors.
    Nevertheless, users can control all parameters for each model. Novice users
    can rely on the default values, while experienced ones can fine-tune deep
    learning models using `sits_tuning`.

Examples:
    from pysits import *

    # Retrieve the set of samples for Mato Grosso
    # fit a training model (rfor model)
    ml_model = sits_train(samples_modis_ndvi, sits_rfor(num_trees=50))
    # get a point and classify the point with the ml_model
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    class_ = sits_classify(
        data=point_ndvi, ml_model=ml_model
    )
