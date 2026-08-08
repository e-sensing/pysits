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

import pytest
from rpy2.rinterface_lib.embedded import RRuntimeError

from pysits.sits.context import samples_l8_rondonia_2bands, samples_modis_ndvi
from pysits.sits.cube import sits_cube
from pysits.sits.data import sits_classify, sits_label_classification
from pysits.sits.ml import sits_pre_train, sits_rfor, sits_ssl_mae, sits_train
from pysits.sits.ts import sits_patterns, sits_som_map
from pysits.sits.utils import r_package_dir, r_set_seed
from pysits.sits.visualization import sits_plot, sits_sankey, sits_view


#
# Fixtures
#
@pytest.fixture(scope="module")
def class_cubes(local_cube, tmp_path_factory):
    """Two single-step classified cubes."""
    r_set_seed(42)
    output_dir = tmp_path_factory.mktemp("sankey")

    # Train a random forest model
    rfor_model = sits_train(samples_modis_ndvi, sits_rfor())

    # Classify the cube
    probs_cube = sits_classify(
        local_cube,
        rfor_model,
        output_dir=output_dir,
        progress=False,
    )

    # Prepare cubes
    return tuple(
        sits_label_classification(
            probs_cube, output_dir=output_dir, version=version, progress=False
        )
        for version in ("v2013", "v2014")
    )


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


def test_representation_learning_visualization(no_plot_window):
    """Test representation learning visualization."""
    rl_model = sits_pre_train(samples_l8_rondonia_2bands, sits_ssl_mae())
    sits_plot(rl_model)


def test_som_visualization(no_plot_window):
    """Test SOM visualization."""
    som = sits_som_map(data=samples_l8_rondonia_2bands)
    sits_plot(som)


def test_cube_visualization(local_cube, no_plot_window):
    """Test cube visualization."""
    sits_plot(local_cube)


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


def test_cube_visualization_leaflet(local_cube, no_browser):
    """Test cube visualization."""
    sits_view(local_cube)


def test_sankey_visualization(class_cubes, no_plot_window):
    """Test sankey visualization of class trajectories."""
    class_2013, class_2014 = class_cubes

    # The diagram is displayed, not returned
    assert (
        sits_sankey(
            class_2013,
            class_2014,
            labels=["2013", "2014"],
            multicores=1,
            progress=False,
        )
        is None
    )


def test_sankey_visualization_cubes_argument(class_cubes, no_plot_window):
    """Test sankey visualization using the ``cubes`` argument."""
    class_2013, class_2014 = class_cubes

    # Cubes can also be given as a list, instead of separate arguments
    assert (
        sits_sankey(
            cubes=[class_2013, class_2014],
            labels=["2013", "2014"],
            title="Trajectories",
            palette="Set2",
            multicores=1,
            progress=False,
        )
        is None
    )


def test_sankey_visualization_invalid_input(class_cubes):
    """Test sankey visualization with cubes defined in an invalid format."""
    class_2013, class_2014 = class_cubes

    # Cubes must be given as separate arguments or via ``cubes``, not both
    with pytest.raises(RRuntimeError, match="not both"):
        sits_sankey(
            class_2013,
            cubes=[class_2013, class_2014],
            multicores=1,
            progress=False,
        )
