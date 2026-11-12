Describe a data cube as a HuggingFace dataset

Data cubes shared on HuggingFace are described by files sits reads to
understand the dataset. They are kept in a "sits" directory of the
repository, so they are not mixed with the other files of the dataset:

- "sits/sits.yml": the collection definition of the dataset;

- "sits/cache.rds": the data cube of the dataset. When it is available,
  sits loads it instead of reading each image of the dataset.

This function writes these files in `output_dir`, as they must be uploaded
to the repository (i.e., the "sits" directory and the images, named as
sits names them, in the root of the repository). Nothing is uploaded by
this function.

The collection definition is written from a data cube: the bands, their
resolution and, for results produced by sits (e.g., probabilities,
classified maps), the labels of the classification.

Each type of cube is described the way sits reads it:

- image raster cubes are described band by band;

- embeddings have only base satellite and sensor described;

- results produced by sits inform only their resolution and the labels
  of the classification.

A dataset can share more than one result of the same classification
(e.g., probabilities and the classified map), which are described
together when they are informed as a list of cubes. A cache describes a
single cube, so it is not written for a list of cubes.

Args:
    cube (SITSCubeModel | list[SITSCubeModel]): Data cube or list of cubes
        to be shared as a dataset.

    output_dir (str | pathlib.Path): Existing directory where the files of
        the dataset are written (optional). When not informed, the
        collection definition is only returned.

    repo (str): HuggingFace repository where the images are uploaded
        ("<user>/<dataset>"). Required to write the cache of a data cube,
        unless the cube was read from HuggingFace.

Returns:
    SITStructureData: Collection definition of the dataset.

Note:
    Images must be named in the dataset as sits names them
    (`sits_cube_copy` and `sits_regularize` do it), and only the bands
    shared in the dataset must be described.

Examples:
    import tempfile
    from pysits import *

    # create a cube
    data_dir = r_package_dir("extdata/raster/mod13q1", package="sits")
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir,
    )

    # get the collection definition of the cube
    collection_conf = sits_to_hf(cube)

    # write the files describing the dataset ("sits/sits.yml" and
    # "sits/cache.rds"), to be uploaded with the images of the cube
    sits_to_hf(
        cube,
        output_dir=tempfile.gettempdir(),
        repo="user/dataset",
    )
