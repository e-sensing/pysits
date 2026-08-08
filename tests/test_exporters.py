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

"""Unit tests for file exporters."""

from pathlib import Path
from zipfile import ZipFile

import pytest

from pysits.backend.pkgs import r_pkg_sits
from pysits.models.data.frame import SITSFrame
from pysits.models.data.matrix import SITSConfusionMatrix
from pysits.sits.context import cerrado_2classes
from pysits.sits.exporters import sits_timeseries_to_csv, sits_to_csv, sits_to_xlsx
from pysits.sits.ml import sits_rfor
from pysits.sits.ts import sits_sample, sits_validate


#
# Helpers
#
def read_xlsx(file: Path) -> dict[str, bytes]:
    """Read the reproducible content of an XLSX file."""
    xlsx_metadata = "docProps/core.xml"

    with ZipFile(file) as workbook:
        return {
            name: workbook.read(name)
            for name in workbook.namelist()
            if name != xlsx_metadata
        }


#
# Fixtures
#
@pytest.fixture(scope="module")
def accuracy() -> SITSConfusionMatrix:
    """Accuracy assessment of a validated model."""
    return sits_validate(
        samples=sits_sample(cerrado_2classes, frac=0.5),
        samples_validation=sits_sample(cerrado_2classes, frac=0.5),
        ml_method=sits_rfor(),
    )


#
# Tests
#
def test_sits_to_csv(tmp_path: Path):
    """Test time-series metadata exported as csv."""
    py_file = tmp_path / "python.csv"
    r_file = tmp_path / "r.csv"

    result = sits_to_csv(cerrado_2classes, file=py_file)
    r_pkg_sits.sits_to_csv(cerrado_2classes._instance, file=str(r_file))

    assert isinstance(result, SITSFrame)
    assert py_file.read_text() == r_file.read_text()


def test_sits_timeseries_to_csv(tmp_path: Path):
    """Test time-series values exported as csv."""
    py_file = tmp_path / "python.csv"
    r_file = tmp_path / "r.csv"

    sits_timeseries_to_csv(cerrado_2classes, file=py_file)
    r_pkg_sits.sits_timeseries_to_csv(cerrado_2classes._instance, file=str(r_file))

    assert py_file.read_text() == r_file.read_text()


def test_sits_to_xlsx(tmp_path: Path, accuracy):
    """Test accuracy assessment exported as xlsx."""
    py_file = tmp_path / "python.xlsx"
    r_file = tmp_path / "r.xlsx"

    sits_to_xlsx(accuracy, file=py_file)
    r_pkg_sits.sits_to_xlsx(accuracy._instance, file=str(r_file))

    assert read_xlsx(py_file) == read_xlsx(r_file)
