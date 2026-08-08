Define a linear formula for classification models

Provides a symbolic description of a fitting model. Tells the model to do a
linear transformation of the input values. The `predictors_index` parameter
informs the positions of fields corresponding to formula independent variables.
If no value is given, that all fields will be used as predictors.

Args:
    predictors_index (list[int]): Index of the valid columns whose names are
        used to compose formula (default: -2:0).

Returns:
    R: A function that computes a valid formula using a linear function.

Examples:
    from pysits import *

    # Example of training a model for time series classification
    # Retrieve the samples for Mato Grosso
    # train an SVM model
    ml_model = sits_train(samples_modis_ndvi,
        ml_method=sits_svm(formula=sits_formula_logref())
    )
    # classify the point
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    # classify the point
    point_class = sits_classify(
        data=point_ndvi, ml_model=ml_model
    )
    plot(point_class)
