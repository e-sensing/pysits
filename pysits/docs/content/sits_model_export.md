Export classification models

Given a trained machine learning or deep learning model, exports the
model as an object for further exploration outside the `sits` package.

Args:
    ml_model (SITSMachineLearningMethod): A trained machine learning
        model.

Returns:
    None: The model in the original format of the machine learning or
        deep learning package.

Examples:
    from pysits import *

    # create a classification model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())
    # export the model
    rfor_object = sits_model_export(rfor_model)
