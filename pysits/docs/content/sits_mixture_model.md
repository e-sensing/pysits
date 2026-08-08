Multiple endmember spectral mixture analysis

Create a multiple endmember spectral mixture analyses fractions images. We use
the non-negative least squares (NNLS) solver to calculate the fractions of each
endmember. The NNLS was implemented by Jakob Schwalb-Willmann in RStoolbox
package (licensed as GPL>=3).

Args:
    data (SITSCubeModel | SITSTimeSeriesModel): A data cube or a set of
        sample time series.
    endmembers (pandas.DataFrame | str | pathlib.Path): Reference spectral
        endmembers (see details below).
    rmse_band (bool): Whether the error associated with the linear model
        should be generated. If `True`, a new band with errors for each
        pixel is generated using the root mean square measure (RMSE).
        Default is `True`.
    multicores (int): Number of cores to be used for generate the mixture
        model.
    progress (bool): Show progress bar? Default is `True`.
    memsize (int): Memory available for the mixture model (in GB).
    output_dir (str | pathlib.Path): Directory for output images.
    **kwargs (dict): Parameters for specific functions.

Returns:
    SITSFrame: In case of a cube, a data cube with the fractions of each
        endmember. The sum of all fractions is restricted to 1 (scaled from
        0 to 10000), corresponding to the abundance of the endmembers in the
        pixels. In case of a set of sample time series, the time series with
        the values corresponding to each fraction.

Notes:
    Many pixels in images of medium-resolution satellites such as Landsat or
    Sentinel-2 contain a mixture of spectral responses of different land cover
    types. In many applications, it is desirable to obtain the proportion of a
    given class inside a mixed pixel. For this purpose, the literature proposes
    mixture models; these models represent pixel values as a combination of
    multiple pure land cover types. Assuming that the spectral response of pure
    land cover classes (called endmembers) is known, spectral mixture analysis
    derives new bands containing the proportion of each endmember inside a
    pixel.
    The `endmembers` parameter should be a `pandas.DataFrame`, csv or a
    shapefile. `endmembers` parameter must have the following columns: `type`,
    which defines the endmembers that will be created and the columns
    corresponding to the bands that will be used in the mixture model. The band
    values must follow the product scale. For example, in the case of
    sentinel-2 images the bands should be in the range 0 to 1. See the
    `example` in this documentation for more details.

Examples:
    from pysits import *
    import pandas as pd
    import tempfile
    import os

    # Create a sentinel-2 cube
    s2_cube = sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        tiles="20LKP",
        bands=["B02", "B03", "B04", "B8A", "B11", "B12", "CLOUD"],
        start_date="2019-06-13",
        end_date="2019-06-30"
    )
    # create a directory to store the regularized file
    reg_dir = os.path.join(tempfile.gettempdir(), "mix_model")
    os.makedirs(reg_dir, exist_ok=True)
    # Cube regularization for 16 days and 160 meters
    reg_cube = sits_regularize(
        cube=s2_cube,
        period="P16D",
        res=160,
        roi={
            "lon_min": -65.54870165,
            "lat_min": -10.63479162,
            "lon_max": -65.07629670,
            "lat_max": -10.36046639
        },
        multicores=2,
        output_dir=reg_dir
    )

    # Create the endmembers tibble
    em = pd.DataFrame({
        "class": ["forest", "land", "water"],
        "B02": [0.02, 0.04, 0.07],
        "B03": [0.0352, 0.065, 0.11],
        "B04": [0.0189, 0.07, 0.14],
        "B8A": [0.28, 0.36, 0.085],
        "B11": [0.134, 0.35, 0.004],
        "B12": [0.0546, 0.18, 0.0026]
    })

    # Generate the mixture model
    mm = sits_mixture_model(
        data=reg_cube,
        endmembers=em,
        memsize=4,
        multicores=2,
        output_dir=tempfile.gettempdir()
    )
