Get time series from data cubes and cloud services

Description:
    Retrieve a set of time series from a data cube and and put the result 
    in a sits tibble, which contains both the satellite image time series 
    and their metadata.

    There are five options for specifying the input samples parameter:

    A CSV file: see sits_get_data.csv.

    A shapefile: see sits_get_data.shp.

    An sf object: see sits_get_data.sf.

    A sits tibble: see sits_get_data.sits.

    A data.frame: see see sits_get_data.data.frame.

Usage:
    sits_get_data(cube, samples, ...)

    ## Default S3 method:
    sits_get_data(cube, samples, ...)

Args:
    cube: 
        Data cube from where data is to be retrieved. 
        (tibble of class "raster_cube").

    samples: 
        Location of the samples to be retrieved. Either a tibble of class 
        "sits", an "sf" object, the name of a shapefile or csv file, or a 
        data.frame with columns "longitude" and "latitude".

    **kwargs: 
        Specific parameters for each input.

Returns:
    A tibble of class "sits" with set of time series 
    <longitude, latitude, start_date, end_date, label, time_series>.

Note:
    The main sits classification workflow has the following steps:

    sits_cube: selects a ARD image collection from a cloud provider.

    sits_cube_copy: copies an ARD image collection from a cloud provider 
    to a local directory for faster processing.

    sits_regularize: create a regular data cube from an ARD image collection.

    sits_apply: create new indices by combining bands of a regular data 
    cube (optional).

    sits_get_data: extract time series from a regular data cube based on 
    user-provided labelled samples.

    sits_train: train a machine learning model based on image time series.

    sits_classify: classify a data cube using a machine learning model and 
    obtain a probability cube.

    sits_smooth: post-process a probability cube using a spatial smoother 
    to remove outliers and increase spatial consistency.

    sits_label_classification: produce a classified map by selecting the 
    label with the highest probability from a smoothed cube.

    To be able to build a machine learning model to classify a data cube, 
    one needs to use a set of labelled time series. These time series are 
    created by taking a set of known samples, expressed as labelled points 
    or polygons. This sits_get_data function uses these samples to extract 
    time series from a data cube. It needs a cube parameter which points to 
    a regularized data cube, and a samples parameter that describes the 
    locations of the training set.

Author(s):
    Felipe Carlos, efelipecarlos@gmail.com

    Felipe Carvalho, felipe.carvalho@inpe.br

    Gilberto Camara, gilberto.camara@inpe.br

    Rolf Simoes, rolfsimoes@gmail.com
