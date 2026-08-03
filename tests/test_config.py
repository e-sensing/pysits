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

"""Unit tests for sits configuration."""

from pathlib import Path

import pytest
from rpy2.rinterface_lib.embedded import RRuntimeError
from rpy2.rinterface_lib.sexp import NULLType

from pysits.backend.loaders import load_function_from_package
from pysits.sits.config import sits_parallel


def _cluster():
    """Get the current sits cluster."""
    return load_function_from_package("sits::sits_parallel")()


@pytest.fixture(autouse=True)
def stop_cluster():
    """Fixture to guarantee no cluster is left open by the tests."""
    yield

    sits_parallel(0)


def test_sits_parallel_start():
    """Test sits parallel cluster creation."""
    assert sits_parallel(2) is None
    assert not isinstance(_cluster(), NULLType)


def test_sits_parallel_restart():
    """Test sits parallel cluster restart."""
    sits_parallel(2)

    assert sits_parallel(3) is None
    assert not isinstance(_cluster(), NULLType)


@pytest.mark.parametrize("workers", [0, 1])
def test_sits_parallel_stop(workers: int):
    """Test sits parallel cluster stop."""
    sits_parallel(2)

    assert sits_parallel(workers) is None
    assert isinstance(_cluster(), NULLType)


def test_sits_parallel_with_log(tmp_path: Path):
    """Test sits parallel cluster creation with log enabled."""
    assert sits_parallel(2, log=True, output_dir=tmp_path.as_posix()) is None
    assert not isinstance(_cluster(), NULLType)


def test_sits_parallel_invalid_workers():
    """Test sits parallel with an invalid number of workers."""
    with pytest.raises(RRuntimeError):
        sits_parallel(-1)


def test_sits_parallel_log_without_output_dir():
    """Test sits parallel with log enabled and no output directory."""
    with pytest.raises(RRuntimeError):
        sits_parallel(2, log=True)
