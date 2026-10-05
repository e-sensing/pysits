Read data cubes, samples and models shared on HuggingFace

Reads data shared in a HuggingFace repository. The content of the
repository defines what is read:

- data cubes: datasets describing a collection in a "sits/sits.yml" file
  (see `sits_to_hf`). The images selected are downloaded to `output_dir`
  and a local data cube is returned;

- samples: time series saved as ".rds" or ".parquet" files (see
  `sits_to_parquet`);

- models: models trained by `sits_train` and saved as ".rds" files.

When `file` is not informed, a repository with a "sits/sits.yml" file is
read as a data cube. Otherwise, the repository must have a single ".rds"
or ".parquet" file. When there are many, choose one using `file`.

Args:
    repo (str): HuggingFace repository ("<user>/<repository>").

    file (str): File to be read in the repository (optional).

    type (str): Type of the repository: "dataset" (default) or "model".
        Data cubes are always shared in datasets.

    bands (list[str]): Bands to be selected in the data cube (optional).

    tiles (list[str]): Tiles to be selected in the data cube (optional).

    roi (dict | geopandas.GeoDataFrame): Region of interest to be selected
        in the data cube (optional).

    crs (str): The Coordinate Reference System (CRS) of the roi.

    start_date (str): Start date of the data cube ("YYYY-MM-DD").

    end_date (str): End date of the data cube ("YYYY-MM-DD").

    output_dir (str | pathlib.Path): Existing directory where the images
        of the data cube are saved (required for data cubes).

    n_tries (int): Number of attempts to download the same image.

    multicores (int): Number of cores for parallel downloading.

    progress (bool): Show progress bar?

    **kwargs: Other parameters to read data cubes: `labels` (dict) and
        `version` (str) select results produced by sits (e.g.,
        probabilities).

Returns:
    SITSCubeModel | SITSTimeSeriesModel | SITSMachineLearningMethod: A data
    cube with local images, a set of samples, or a model.

Note:
    HuggingFace limits the number of files a user requests in windows of
    five minutes. For this reason, the images of a data cube are
    downloaded, each one requested only once, in batches that fit the
    requests available. When no request is available, the download waits
    the next window. Images already downloaded in `output_dir` are not
    requested again, so an interrupted download is resumed by calling
    `sits_from_hf` again.

    To access private repositories, the HuggingFace access token must be
    set in the `HF_TOKEN` environment variable.

Examples:
    import tempfile
    from pysits import *

    # download a data cube shared in a HuggingFace dataset
    cube = sits_from_hf(
        repo="felipemcarlos/sits_mod13q1_sinop",
        output_dir=tempfile.gettempdir(),
    )

    # read samples shared in a HuggingFace dataset
    samples = sits_from_hf(repo="felipemcarlos/sits_samples_modis_ndvi")

    # read a model shared in a HuggingFace model repository
    model = sits_from_hf(
        repo="felipemcarlos/sits_rfor_modis_ndvi", type="model"
    )
