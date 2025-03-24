#
# Copyright (C) 2025 sits developers.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#

"""cube operations."""

from pysits import types as type_utils
from pysits.backend.sits import r_sits
from pysits.models import SITSCubeModel


#
# High-level operations
#
@type_utils.rpy2_fix_type
def sits_cube(*args, **kwargs):
    """Create cubes.

     Creates a data cube based on spatial and temporal restrictions
     from image collections available in cloud services or local
     repositories.

     Supports multiple cloud providers based on the STAC protocol, including:

        - Amazon Web Services (AWS)
        - Brazil Data Cube (BDC)
        - Copernicus Data Space Ecosystem (CDSE)
        - Digital Earth Africa (DEAFRICA)
        - Digital Earth Australia (DEAUSTRALIA)
        - Microsoft Planetary Computer (MPC)
        - NASA Harmonized Landsat/Sentinel (HLS)
        - Swiss Data Cube (SDC)
        - TERRASCOPE
        - USGS Landsat (USGS)

        Data cubes can also be created from local files.

    Args:
        source (str):
            Data source, must be one of:
            `"AWS"`, `"BDC"`, `"CDSE"`, `"DEAFRICA"`, `"DEAUSTRALIA"`,
            `"HLS"`, `"MPC"`, `"SDC"`, `"TERRASCOPE"`, `"USGS"`.

        collection (str):
            Image collection in the selected data source. Use `sits_list_collections()`
            to find available collections.

        platform (str, optional):
            Specifies the platform when collections include multiple satellites.

        tiles (list, optional):
            List of tiles from the collection to include in the cube.

        roi (dict, optional):
            Region of interest. Can be:
            - `sf` object
            - Shapefile
            - `SpatExtent`
            - Dictionary with named coordinates:
                - `"xmin"`, `"xmax"`, `"ymin"`, `"ymax"`
                - `"lon_min"`, `"lat_min"`, `"lon_max"`, `"lat_max"`

        crs (str, optional):
            The Coordinate Reference System (CRS) of the `roi`. Required if `roi`
            uses XY values or `SpatExtent`.

        bands (list, optional):
            List of spectral bands and indices to include in the cube.

        orbit (str, optional):
            Orbit name for SAR cubes (`"ascending"`, `"descending"`).

        vector_band (str, optional):
            Band for vector cubes (`"segments"`, `"probs"`, `"class"`).

        start_date (str, optional):
            Start date for selecting images in `"YYYY-MM-DD"` format.

        end_date (str, optional):
            End date for selecting images in `"YYYY-MM-DD"` format.

        data_dir (str, optional):
            Local directory where images are stored (for local cubes).

        vector_dir (str, optional):
            Local directory where vector files are stored (for local vector cubes).

        parse_info (list, optional):
            Parsing information for extracting metadata from local file names.

        version (str, optional):
            Version of the classified and/or labeled files.

        delim (str, optional):
            Delimiter character for parsing local file names.

        labels (dict, optional):
            Labels associated with classification results (for `probs_cube` or
            `class_cube`).

        multicores (int, optional):
            Number of workers for parallel processing. Must be between 1 and
            2048. Default is `1`.

        progress (bool, optional):
            Whether to display a progress bar. Default is `False`.

        **kwargs:
            Additional parameters for specific data cube configurations.

    Returns:
        pd.DataFrame: A DataFrame describing the contents of the data cube.

    Notes:
        - To create cubes from cloud providers, you must specify:
          - `source`
          - `collection`
          - `tiles` or `roi`
        - The `roi` parameter selects images but does **not** crop them.
        - You can use GeoJSON geometries as `roi` by converting them to an `sf` object.
        - `sits` supports various cloud providers and multiple collections.
        - For local cubes, `data_dir` and `parse_info` must be specified.

    Examples:
        Creating a data cube from the **Brazil Data Cube (BDC)**:
        ```python
        cbers_tile = sits_cube(
            source="BDC",
            collection="CBERS-WFI-16D",
            bands=["NDVI", "EVI"],
            tiles=["007004"],
            start_date="2018-09-01",
            end_date="2019-08-28"
        )
        ```

        Creating a cube from **Digital Earth Africa (DEAFRICA)**:
        ```python
            cube_deafrica = sits_cube(
                source="DEAFRICA",
                collection="SENTINEL-2-L2A",
                bands=["B04", "B08"],
                roi={
                    "lat_min": 17.379,
                    "lon_min": 1.1573,
                    "lat_max": 17.410,
                    "lon_max": 1.1910
                },
                start_date="2019-01-01",
                end_date="2019-10-28"
            )
        ```

        Creating a **Sentinel-2 cube from AWS**:
        ```python
            s2_cube = sits_cube(
                source="AWS",
                collection="SENTINEL-S2-L2A-COGS",
                tiles=["20LKP", "20LLP"],
                bands=["B04", "B08", "B11"],
                start_date="2018-07-18",
                end_date="2019-07-23"
            )
        ```
    """
    cube = r_sits.sits_cube(*args, **kwargs)
    return SITSCubeModel(cube)


@type_utils.rpy2_fix_type
def sits_regularize(*args, **kwargs):
    """Build a regular data cube from an irregular one.

    Produces regular data cubes for analysis-ready data (ARD) image collections.
    Analysis-ready data (ARD) collections available in AWS, MPC, USGS and DEAfrica
    are not regular in space and time. Bands may have different resolutions, images
    may not cover the entire time, and time intervals are not regular. For this
    reason, subsets of these collection need to be converted to regular data cubes
    before further processing and data analysis. This function requires users to
    include the cloud band in their ARD-based data cubes.
    """
    cube = r_sits.sits_regularize(*args, **kwargs)
    return SITSCubeModel(cube)


@type_utils.rpy2_fix_type
def sits_cube_copy(*args, **kwargs):
    """Copy cubes.

    This function copies images of a cube in parallel. A region of
    interest (roi) can be provided to crop the images
    and a resolution (res) to resample the bands.

    ToDo:
        - Requires a data cube as input.
    """
    cube = r_sits.sits_cube_copy(*args, **kwargs)
    return SITSCubeModel(cube)
