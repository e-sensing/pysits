Describe a collection of sits as a HuggingFace dataset

Data cubes shared on HuggingFace are described by a "sits/sits.yml" file
in the dataset repository, which sits reads to open the dataset.

This function writes that description from a collection registered in
sits (see `sits_list_collections`), which is useful when a dataset shares
images of a known collection (e.g., images of "SENTINEL-2-L2A" downloaded
from "MPC").

The description of a collection is written as the dataset needs it: the
bands are named as sits names them in the images, and the properties used
by sits to reach the provider are not written, as sits defines them when
it registers a dataset.

Args:
    source (str): Data source.

    collection (str): Image collection.

    bands (list[str]): Bands shared in the dataset (default is all of
        them).

    output_dir (str | pathlib.Path): Existing directory where the file
        "sits/sits.yml" is written (optional). When not informed, the
        collection definition is only returned.

Returns:
    SITStructureData: Collection definition of the dataset.

Note:
    A dataset must describe only the bands it holds, and the resolution of
    each band is the one the collection declares. If you need to describe
    a regularized cube, or a cube with custom bands, use `sits_to_hf`.

Examples:
    import tempfile
    from pysits import *

    # describe a collection as a HuggingFace dataset
    sits_config_to_hf(
        source="MPC",
        collection="SENTINEL-2-L2A",
        bands=["B02", "B03", "B04", "B08"],
        output_dir=tempfile.gettempdir(),
    )
