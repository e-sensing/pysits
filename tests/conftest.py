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

"""Pytest configuration file."""

import webbrowser
from typing import Any

import matplotlib

#
# Set the backend to avoid plot windows
#
matplotlib.use("Agg")

#
# Import after setting visualization backend
#
import matplotlib.pyplot as plt
import pytest
import rpy2.robjects as ro

from pysits.models.data.cube import SITSCubeModel
from pysits.sits.cube import sits_cube
from pysits.sits.utils import r_package_dir


#
# Helpers
#
def r_closure_value(method: Any, name: str) -> Any:
    """Read a value stored in the R closure of a ml/dl method."""
    return ro.r["environment"](method)[name]


def r_opt_hparams(method: Any) -> dict[str, float]:
    """Read the optimizer hyperparameters of a ml/dl method."""
    hparams = r_closure_value(method, "opt_hparams")

    return {k: v[0] for k, v in zip(hparams.names, hparams, strict=True)}


def r_class(obj: Any) -> list[str]:
    """Read the classes of an R object."""
    return list(ro.r["class"](obj))


def r_identical(x: Any, y: Any) -> bool:
    """Check if two R objects are identical."""
    return bool(ro.r["identical"](x, y)[0])


#
# Fixtures
#
@pytest.fixture(scope="module")
def local_cube() -> SITSCubeModel:
    """Cube created from local files."""
    return sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=r_package_dir("extdata/raster/mod13q1", package="sits"),
        progress=False,
    )


@pytest.fixture
def no_plot_window(monkeypatch):
    """Fixture to prevent matplotlib plot windows from showing during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)

    yield

    plt.close("all")


@pytest.fixture
def no_browser(monkeypatch):
    """Fixture to prevent webbrowser from opening during tests."""
    monkeypatch.setattr(webbrowser, "open", lambda x: None)
    monkeypatch.setattr(webbrowser, "open_new", lambda x: None)
    monkeypatch.setattr(webbrowser, "open_new_tab", lambda x: None)

    yield
