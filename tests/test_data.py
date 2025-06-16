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

"""Unit tests for data operations (cube and time-series)."""

from pathlib import Path

from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube, sits_regularize
from pysits.sits.data import (
    sits_apply,
    sits_bands,
    sits_merge,
    sits_reduce,
    sits_select,
    sits_timeline,
)
from pysits.sits.utils import r_package_dir


def test_cube_select():
    """Test cube select."""

    cube = sits_cube(
        source="BDC",
        collection="CBERS-WFI-16D",
        bands=("NDVI", "EVI"),
        tiles="007004",
        start_date="2018-09-01",
        end_date="2019-08-28",
    )

    # Select bands
    cube_ndvi = sits_select(cube, bands="NDVI")
    assert isinstance(cube_ndvi, SITSCubeModel)
    assert sits_bands(cube_ndvi) == ["NDVI"]

    # Select time
    cube_ndvi_short = sits_select(
        cube_ndvi, start_date="2018-08-29", end_date="2019-01-01"
    )
    assert len(sits_timeline(cube_ndvi_short)) == 9  # noqa: PLR2004


def test_sits_select():
    """Test sits select."""

    # Select bands
    samples_evi = sits_select(samples_l8_rondonia_2bands, bands="EVI")
    assert isinstance(samples_evi, SITSTimeSeriesModel)
    assert sits_bands(samples_evi) == ["EVI"]

    # Select time
    samples_evi_short = sits_select(
        samples_evi, start_date="2019-01-17", end_date="2019-07-12"
    )
    assert len(sits_timeline(samples_evi_short)) == 12  # noqa: PLR2004


def test_merge_cubes(tmp_path: Path):
    """Test merging of Sentinel-1 and Sentinel-2 cubes."""
    dir1 = tmp_path / "s1"
    dir2 = tmp_path / "s2"
    dir1.mkdir(parents=True, exist_ok=True)
    dir2.mkdir(parents=True, exist_ok=True)

    # Create Sentinel-1 RTC cube
    cube_s1_rtc = sits_cube(
        source="MPC",
        collection="SENTINEL-1-RTC",
        bands=("VV", "VH"),
        orbit="descending",
        tiles=("22LBL"),
        start_date="2021-06-01",
        end_date="2021-10-01",
        progress=False,
    )

    # Create Sentinel-2 cube
    cube_s2 = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        bands=("B02", "B8A", "B11", "CLOUD"),
        tiles=("22LBL"),
        start_date="2021-06-01",
        end_date="2021-09-30",
        progress=False,
    )

    # Regularize Sentinel-1 cube
    cube_s1_reg = sits_regularize(
        cube=cube_s1_rtc,
        period="P16D",
        res=540,
        tiles=("22LBL"),
        memsize=4,
        multicores=4,
        output_dir=dir2,
        progress=False,
    )

    # Regularize Sentinel-2 cube
    cube_s2_reg = sits_regularize(
        cube=cube_s2,
        period="P16D",
        res=540,
        memsize=4,
        multicores=4,
        output_dir=dir1,
        progress=False,
    )

    # Merge the regularized cubes
    cube_s1_s2 = sits_merge(cube_s2_reg, cube_s1_reg)

    # Verify the result is a SITSCubeModel
    assert isinstance(cube_s1_s2, SITSCubeModel)

    # Check that the merged cube contains all bands
    merged_bands = sits_bands(cube_s1_s2)
    assert all(band in merged_bands for band in ["VV", "VH", "B02", "B8A", "B11"])

    # Check tiles
    assert cube_s1_s2["tile"].iloc[0] == "22LBL"

    # Check timeline
    timeline = sits_timeline(cube_s1_s2)
    assert len(timeline) > 0  # Should have at least one date
    assert min(timeline) >= "2021-06-01"
    assert max(timeline) <= "2021-09-22"


def test_sits_apply():
    """Test sits apply."""
    points = sits_select(samples_l8_rondonia_2bands, bands="NDVI")
    points_norm = sits_apply(
        points, NDVI_norm="(NDVI - min(NDVI)) / (max(NDVI) - min(NDVI))"
    )

    points_nonnorm = sits_apply(
        points,
        NDVI_nonnorm="(NDVI - min(NDVI)) / (max(NDVI) - min(NDVI))",
        normalized=False,
    )

    assert all(band in sits_bands(points_norm) for band in ["NDVI", "NDVI_norm"])
    assert all(band in sits_bands(points_nonnorm) for band in ["NDVI", "NDVI_nonnorm"])


def test_cube_apply(tmp_path: Path):
    """Test cube apply."""
    data_dir = r_package_dir(
        "extdata/raster/mod13q1",
        package="sits",
    )
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir,
    )

    # Generate a texture images with variance in NDVI images
    cube_texture = sits_apply(
        data=cube, NDVITEXTURE="w_median(NDVI)", window_size=5, output_dir=tmp_path
    )

    assert all(band in sits_bands(cube_texture) for band in ["NDVI", "NDVITEXTURE"])


def test_sits_reduce():
    """Test reduce in samples."""
    points = sits_select(samples_l8_rondonia_2bands, "NDVI")
    points_reduced = sits_reduce(points, NDVI_MEDIAN="t_median(NDVI)")

    assert "NDVI-MEDIAN" in sits_bands(points_reduced)
    assert len(sits_timeline(points_reduced)) == 1  # noqa: PLR2004 - one date


def test_cube_reduce(tmp_path: Path):
    """Test reduce in cube."""
    data_dir = r_package_dir(
        "extdata/raster/mod13q1",
        package="sits",
    )
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=data_dir,
    )

    # Reduce the cube
    cube_reduced = sits_reduce(
        cube,
        NDVIMEAN="t_mean(NDVI)",
        output_dir=tmp_path,
        progress=False,
        multicores=2,
    )

    # Check cube properties
    assert "NDVIMEAN" in sits_bands(cube_reduced)
    assert len(sits_timeline(cube_reduced)) == 1  # noqa: PLR2004 - one date
