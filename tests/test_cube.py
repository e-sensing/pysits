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

"""Unit tests for cube operations."""

from pathlib import Path

from pandas import DataFrame as PandasDataFrame

from pysits.conversions.dsl.mask import MaskValue
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.frame import SITSFrame
from pysits.sits.cube import sits_cube, sits_reclassify
from pysits.sits.data import sits_bands, sits_bbox, sits_labels, sits_timeline
from pysits.sits.utils import r_package_dir


def test_sits_cube_data_structure():
    """Test data structure of sits_cube."""
    # Define a region of interest for the city of Sinop
    roi_sinop = {
        "lon_min": -56.87417,
        "lon_max": -54.63718,
        "lat_min": -12.17083,
        "lat_max": -11.02292,
    }

    # Call sits_cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        bands=["NDVI", "EVI"],
        roi=roi_sinop,
        start_date="2013-09-14",
        end_date="2014-08-29",
        progress=False,
    )

    # Verify the result is a SITSCubeModel
    assert isinstance(cube, SITSCubeModel)

    # Check columns
    assert all(
        col in cube.columns
        for col in [
            "source",
            "collection",
            "satellite",
            "sensor",
            "tile",
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "crs",
            "file_info",
        ]
    )

    # Check bands
    cube_bands = sits_bands(cube)
    assert all(band in cube_bands for band in ["NDVI", "EVI"])

    # Check timeline
    cube_timeline = sits_timeline(cube)
    assert len(cube_timeline) == 23  # noqa: PLR2004


def test_sits_cube_bbox():
    """Test bbox of sits cube."""
    # Define a region of interest for the city of Sinop
    roi_sinop = {
        "lon_min": -56.87417,
        "lon_max": -54.63718,
        "lat_min": -12.17083,
        "lat_max": -11.02292,
    }

    # Create a cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        bands=["NDVI", "EVI"],
        roi=roi_sinop,
        start_date="2013-09-14",
        end_date="2014-08-29",
        progress=False,
    )

    # Get bbox
    bbox = sits_bbox(cube)

    # Check bbox structure
    assert isinstance(bbox, SITSFrame)
    assert all(col in bbox.columns for col in ["xmin", "xmax", "ymin", "ymax"])

    # Check crs transformation
    bbox_4326 = sits_bbox(cube, as_crs="EPSG:4326")
    bbox_4326 = bbox_4326.iloc[0]

    assert round(bbox_4326["xmin"], 4) == -63.8507  # noqa: PLR2004
    assert round(bbox_4326["xmax"], 4) == -50.7713  # noqa: PLR2004
    assert round(bbox_4326["ymin"], 4) == -20.0  # noqa: PLR2004
    assert round(bbox_4326["ymax"], 4) == -10.0  # noqa: PLR2004
    assert bbox_4326["crs"] == "EPSG:4326"


def test_sits_cube_filter():
    """Test filtering of sits cube."""
    cube = sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        tiles=("20LLP", "20LKP"),
        bands=("B02", "B8A", "B11", "CLOUD"),
        start_date="2018-06-30",
        end_date="2018-08-31",
    )

    cube_tile1 = cube.query('tile == "20LLP"')
    assert isinstance(cube_tile1, SITSCubeModel)
    assert cube_tile1.tile.iloc[0] == "20LLP"
    assert not isinstance(cube_tile1._instance, PandasDataFrame)

    cube_tile2 = cube.query('tile == "20LKP"')
    assert isinstance(cube_tile2, SITSCubeModel)
    assert cube_tile2.tile.iloc[0] == "20LKP"
    assert not isinstance(cube_tile2._instance, PandasDataFrame)


def s(tmp_path: Path):
    """Test reclassify of classified cube."""
    # Open mask map
    data_dir = r_package_dir("extdata/raster/prodes", package="sits")
    prodes2021 = sits_cube(
        source="USGS",
        collection="LANDSAT-C2L2-SR",
        data_dir=data_dir,
        parse_info=("X1", "X2", "tile", "start_date", "end_date", "band", "version"),
        bands="class",
        version="v20220606",
        labels={
            "1": "Forest",
            "2": "Water",
            "3": "NonForest",
            "4": "NonForest2",
            "6": "d2007",
            "7": "d2008",
            "8": "d2009",
            "9": "d2010",
            "10": "d2011",
            "11": "d2012",
            "12": "d2013",
            "13": "d2014",
            "14": "d2015",
            "15": "d2016",
            "16": "d2017",
            "17": "d2018",
            "18": "r2010",
            "19": "r2011",
            "20": "r2012",
            "21": "r2013",
            "22": "r2014",
            "23": "r2015",
            "24": "r2016",
            "25": "r2017",
            "26": "r2018",
            "27": "d2019",
            "28": "r2019",
            "29": "d2020",
            "31": "r2020",
            "32": "Clouds2021",
            "33": "d2021",
            "34": "r2021",
        },
        progress=False,
    )

    # Open classification map
    data_dir = r_package_dir("extdata/raster/classif", package="sits")
    ro_class = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        data_dir=data_dir,
        parse_info=("X1", "X2", "tile", "start_date", "end_date", "band", "version"),
        bands="class",
        labels={
            "1": "ClearCut_Fire",
            "2": "ClearCut_Soil",
            "3": "ClearCut_Veg",
            "4": "Forest",
        },
        progress=False,
    )

    # Reclassify
    ro_mask = sits_reclassify(
        cube=ro_class,
        mask=prodes2021,
        rules=dict(
            Old_Deforestation=MaskValue.in_(
                [
                    "d2007",
                    "d2008",
                    "d2009",
                    "d2010",
                    "d2011",
                    "d2012",
                    "d2013",
                    "d2014",
                    "d2015",
                    "d2016",
                    "d2017",
                    "d2018",
                    "r2010",
                    "r2011",
                    "r2012",
                    "r2013",
                    "r2014",
                    "r2015",
                    "r2016",
                    "r2017",
                    "r2018",
                    "d2019",
                    "r2019",
                    "d2020",
                    "r2020",
                    "r2021",
                ]
            ),
            Water_Mask=(MaskValue == "Water"),
            NonForest_Mask=MaskValue.in_(["NonForest", "NonForest2"]),
        ),
        memsize=4,
        multicores=2,
        output_dir=tmp_path,
        version="ex_reclassify",
    )

    assert isinstance(ro_mask, SITSCubeModel)
    assert ro_mask.shape[0] == 1  # noqa: PLR2004 - number of tiles
    assert len(sits_labels(ro_mask)) == 5  # noqa: PLR2004 - number of labels
