Sampling random points in a data cube

Takes a random sample of locations in a data cube

Args:
    cube (SITSCubeModel): Data cube.
    n_samples (int): Number of points to be sampled.
    multicores (int): Number of cores used to sample the images in
        parallel.
    memsize (int): Memory available for sampling.
    progress (bool): Show progress bar? Default is `True`.

Returns:
    SITSFrameSF: sample locations.

Examples:
    from pysits import *

    # create a data cube from local files
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir
    )
    # sample for data cube
    samples = sits_random_sampling(
        cube=cube,
        n_samples=100
    )
