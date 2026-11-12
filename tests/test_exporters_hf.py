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

"""Unit tests for HuggingFace export operations."""

from pathlib import Path

import httpx2
import pytest

from pysits.backend.pkgs import r_pkg_sits
from pysits.models.data.base import SITStructureData
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.models.ml import SITSMachineLearningMethod
from pysits.sits.exporters import sits_config_to_hf, sits_from_hf, sits_to_hf


#
# Helpers
#
def list_files(directory: Path) -> list[str]:
    """List the files of a directory."""
    return sorted(
        file.relative_to(directory).as_posix()
        for file in directory.rglob("*")
        if file.is_file()
    )


#
# Fixtures
#
@pytest.fixture(scope="module")
def hf_online() -> None:
    """Skip the tests of a module when HuggingFace is not accessible."""
    try:
        httpx2.head("https://huggingface.co", follow_redirects=True)

    except httpx2.HTTPError:
        pytest.skip("HuggingFace is not accessible")


#
# Tests
#
def test_sits_to_hf(local_cube, tmp_path: Path):
    """Test data cube described as a HuggingFace dataset."""
    py_dir = tmp_path / "python"
    r_dir = tmp_path / "r"
    list_dir = tmp_path / "list"

    for directory in (py_dir, r_dir, list_dir):
        directory.mkdir()

    # single cube, definition and cache are written
    result = sits_to_hf(local_cube, output_dir=py_dir, repo="user/dataset")
    r_pkg_sits.sits_to_hf(
        local_cube._instance, output_dir=str(r_dir), repo="user/dataset"
    )

    # validate the results
    assert isinstance(result, SITStructureData)
    assert list_files(py_dir) == ["sits/cache.rds", "sits/sits.yml"]

    # read the results
    result_py = (py_dir / "sits/sits.yml").read_text()
    result_r = (r_dir / "sits/sits.yml").read_text()

    assert result_py == result_r

    # convert list of cubes
    sits_to_hf([local_cube], output_dir=list_dir)

    # test - only the definition is written, cache is not supported
    assert list_files(list_dir) == ["sits/sits.yml"]


def test_sits_config_to_hf(tmp_path: Path):
    """Test collection described as a HuggingFace dataset."""
    py_dir = tmp_path / "python"
    r_dir = tmp_path / "r"

    for directory in (py_dir, r_dir):
        directory.mkdir()

    # convert collection
    result = sits_config_to_hf(
        source="MPC",
        collection="SENTINEL-2-L2A",
        bands=["B02", "B03"],
        output_dir=py_dir,
    )

    # convert collection in R
    r_pkg_sits.sits_config_to_hf(
        source="MPC",
        collection="SENTINEL-2-L2A",
        bands=["B02", "B03"],
        output_dir=str(r_dir),
    )

    # validate the results
    assert isinstance(result, SITStructureData)
    assert list_files(py_dir) == ["sits/sits.yml"]

    # read the results
    result_py = (py_dir / "sits/sits.yml").read_text()
    result_r = (r_dir / "sits/sits.yml").read_text()

    assert result_py == result_r


@pytest.mark.parametrize(
    "repo, options, expected",
    [
        (
            "felipemcarlos/sits_mod13q1_sinop",
            {"start_date": "2013-09-14", "end_date": "2013-10-16"},
            SITSCubeModel,
        ),
        ("felipemcarlos/sits_samples_modis_ndvi", {}, SITSTimeSeriesModel),
        (
            "felipemcarlos/sits_rfor_modis_ndvi",
            {"type": "model"},
            SITSMachineLearningMethod,
        ),
    ],
)
def test_sits_from_hf(hf_online, tmp_path: Path, repo: str, options: dict, expected):
    """Test data cube, samples and model read from HuggingFace."""
    result = sits_from_hf(
        repo,
        output_dir=tmp_path,
        progress=False,
        **options,
    )

    # validate the results
    assert isinstance(result, expected)
