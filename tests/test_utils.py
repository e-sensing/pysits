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

"""Unit tests for sits utils."""

from pathlib import Path

import pytest

from pysits.backend.loaders import load_function_from_package
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.sits.context import samples_modis_ndvi
from pysits.sits.utils import (
    r_package_dir,
    r_set_seed,
    read_rds,
)


def test_r_set_seed():
    """Test r_set_seed."""
    assert r_set_seed(42) is None


def test_read_rds(tmp_path: Path):
    """Test read RDS compatible with SITS."""
    r_fnc_save_rds = load_function_from_package("base::saveRDS")

    # Create a temporary file
    rds_file = tmp_path / "samples_deforestation.rds"

    # Save RDS
    r_fnc_save_rds(samples_modis_ndvi._instance, rds_file.as_posix())

    # Read RDS
    rds_content = read_rds(rds_file)

    # Save RDS
    assert isinstance(rds_content, SITSTimeSeriesModel)


def test_read_rds_file_not_found():
    """Test read RDS file not found."""
    with pytest.raises(FileNotFoundError):
        read_rds("non-existing-file.rds")


def test_r_package_dir():
    """Test get package dir from an existing R package."""
    assert r_package_dir("extdata/raster/mod13q1", package="sits")
