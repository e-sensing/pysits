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

from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube
from pysits.sits.ml import sits_rfor, sits_train
from pysits.sits.ts import sits_patterns, sits_som_map
from pysits.sits.utils import r_package_dir
from pysits.sits.visualization import sits_plot, sits_view


def test_sits_visualization(no_plot_window):
    """Test sits visualization."""
    sits_plot(samples_l8_rondonia_2bands)


def test_sits_patterns_visualization(no_plot_window):
    """Test sits patterns visualization."""
    patterns = sits_patterns(samples_l8_rondonia_2bands)
    sits_plot(patterns)


def test_machine_learning_visualization(no_plot_window):
    """Test machine learning visualization."""
    ml_model = sits_train(samples_l8_rondonia_2bands, sits_rfor())
    sits_plot(ml_model)


def test_som_visualization(no_plot_window):
    """Test SOM visualization."""
    som = sits_som_map(data=samples_l8_rondonia_2bands)
    sits_plot(som)


def test_cube_visualization(no_plot_window):
    """Test cube visualization."""
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=r_package_dir("extdata/raster/mod13q1", package="sits"),
    )

    sits_plot(cube)


def test_classified_cube_visualization(no_plot_window):
    """Test classified cube visualization."""
    data_dir = r_package_dir("extdata/raster/classif", package="sits")
    cube = sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        data_dir=data_dir,
        parse_info=(
            "X1",
            "X2",
            "tile",
            "start_date",
            "end_date",
            "band",
            "version",
        ),
        bands="class",
        labels={
            "1": "ClearCut_Fire",
            "2": "ClearCut_Soil",
            "3": "ClearCut_Veg",
            "4": "Forest",
        },
        progress=False,
    )

    # Plot the result
    sits_plot(cube)


def test_sits_visualization_leaflet(no_browser):
    """Test sits visualization."""
    sits_view(samples_l8_rondonia_2bands)


def test_cube_visualization_leaflet(no_browser):
    """Test cube visualization."""
    # Create a cube
    cube = sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=r_package_dir("extdata/raster/mod13q1", package="sits"),
    )

    # Plot the cube
    sits_view(cube)
