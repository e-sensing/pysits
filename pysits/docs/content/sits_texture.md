Apply a set of texture measures on a data cube.

A set of texture measures based on the Grey Level Co-occurrence Matrix
(GLCM) described by Haralick. Our implementation follows the guidelines
and equations described by Hall-Beyer (both are referenced below).

The spatial relation between the central pixel and its neighbor is
expressed in radians values, where: #'
- `0`: corresponds to the neighbor on right-side
- `pi/4`: corresponds to the neighbor on the top-right diagonals
- `pi/2`: corresponds to the neighbor on above
- `3*pi/4`: corresponds to the neighbor on the top-left diagonals
Our implementation relies on a symmetric co-occurrence matrix, which
considers the opposite directions of an angle. For example, the neighbor
pixels based on `0` angle rely on the left and right direction; the
neighbor pixels of `pi/2` are above and below the central pixel, and so
on. If more than one angle is provided, we compute their average.

Args:
    cube (SITSCubeModel): Valid data cube.
    window_size (int): An odd number representing the size of the
        sliding window.
    angles (float | list[float]): The direction angles in radians
        related to the central pixel and its neighbor (see details).
        Default is 0.
    memsize (int): Memory available for classification (in GB).
    multicores (int): Number of cores to be used for classification.
    output_dir (str | pathlib.Path): Directory where files will be
        saved.
    progress (bool): Show progress bar?
    **kwargs (dict): GLCM function (see details).

Returns:
    SITSCubeModel: A data cube with new bands, produced according to
        the requested measure.

Examples:
    from pysits import *
    import tempfile

    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )

    # Compute the NDVI variance
    cube_texture = sits_texture(
        cube=cube,
        NDVIVAR="glcm_variance(NDVI)",
        window_size=5,
        output_dir=tempfile.mkdtemp()
    )
