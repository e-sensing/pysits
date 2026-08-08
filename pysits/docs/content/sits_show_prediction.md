Shows the predicted labels for a classified time series

This function takes a classified time series produced by a machine
learning method and displays the result.

Args:
    class (SITSTimeSeriesModel): A time series that has been classified.

Returns:
    SITSFrame: Table with the columns "from", "to", "class".

Examples:
    from pysits import *

    # Retrieve the samples for Mato Grosso
    # train an SVM model
    ml_model = sits_train(samples_modis_ndvi, ml_method=sits_svm)
    # classify the point
    point_ndvi = sits_select(point_mt_6bands, bands="NDVI")
    point_class = sits_classify(
        data=point_ndvi, ml_model=ml_model
    )
    sits_show_prediction(point_class)
