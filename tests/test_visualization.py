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

"""Unit tests for visualization operations."""

import matplotlib

#
# Set the backend to avoid plot windows
#
matplotlib.use("Agg")

#
# Import after setting the backend
#
import matplotlib.pyplot as plt
import pytest

from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube
from pysits.sits.utils import get_package_dir
from pysits.sits.visualization import sits_plot


@pytest.fixture
def no_plot_window(monkeypatch):
    """Fixture to prevent matplotlib plot windows from showing during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


def test_cube_visualization(no_plot_window):
    """Test cube visualization."""
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=get_package_dir("extdata/raster/mod13q1", package="sits"),
    )

    sits_plot(cube)


def test_sits_visualization(no_plot_window):
    """Test sits visualization."""
    sits_plot(samples_l8_rondonia_2bands)
