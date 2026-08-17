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

from io import BytesIO
from pathlib import Path

import matplotlib
import pytest
from PIL import Image
from rpy2.rinterface_lib.embedded import RRuntimeError

from pysits.models.visual import SITSPlot, SITSPlotList
from pysits.sits.context import (
    cerrado_2classes,
    point_mt_6bands,
    samples_l8_rondonia_2bands,
    samples_modis_ndvi,
)
from pysits.sits.cube import sits_cube
from pysits.sits.data import sits_classify, sits_label_classification
from pysits.sits.ml import sits_pre_train, sits_rfor, sits_ssl_mae, sits_train
from pysits.sits.ts import sits_patterns, sits_som_map
from pysits.sits.utils import r_package_dir, r_set_seed
from pysits.sits.visualization import sits_plot, sits_sankey, sits_view
from pysits.visualization import base
from pysits.visualization.options import set_plot_options

#
# Constants
#
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


#
# Helpers
#
def assert_is_figure(plot: object) -> SITSPlot | SITSPlotList:
    """Assert that a plot result carries usable PNG figures."""
    # Check type
    assert isinstance(plot, SITSPlot | SITSPlotList)

    # Get figures
    figures = [plot] if isinstance(plot, SITSPlot) else list(plot)

    # Check each figure
    for figure in figures:
        # Check data
        assert figure.data.startswith(PNG_SIGNATURE)
        assert Image.open(BytesIO(figure.data)).size == figure.options.pixel_size

        # Get representation values
        payload, metadata = figure._repr_png_()
        width, height = figure.options.display_size

        # Check representation
        assert payload is figure.data
        assert metadata == {"width": width, "height": height}

    # Return!
    return plot


def assert_is_single_figure(plot: object) -> SITSPlot:
    """Assert that a plot result is one figure."""
    assert isinstance(assert_is_figure(plot), SITSPlot)

    return plot


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


def test_sits_visualization():
    """Test sits visualization."""
    # Plot the result
    plots = assert_is_figure(sits_plot(samples_l8_rondonia_2bands))

    # Check type and length
    assert isinstance(plots, SITSPlotList)
    assert len(plots) > 1


def test_sits_visualization_single_figure():
    """Test samples that produce a single figure."""
    assert_is_single_figure(sits_plot(point_mt_6bands))


def test_sits_patterns_visualization():
    """Test sits patterns visualization."""
    patterns = sits_patterns(samples_l8_rondonia_2bands)

    assert_is_figure(sits_plot(patterns))


def test_machine_learning_visualization():
    """Test machine learning visualization."""
    ml_model = sits_train(samples_l8_rondonia_2bands, sits_rfor())

    assert_is_figure(sits_plot(ml_model))


def test_representation_learning_visualization():
    """Test representation learning visualization."""
    rl_model = sits_pre_train(samples_l8_rondonia_2bands, sits_ssl_mae())

    assert_is_figure(sits_plot(rl_model))


def test_som_visualization(tmp_path, monkeypatch):
    """Test SOM visualization."""
    # Change working directory
    monkeypatch.chdir(tmp_path)

    # Plot the result
    som = sits_som_map(data=samples_l8_rondonia_2bands)

    # Check that the figure is valid
    assert_is_figure(sits_plot(som))

    # Check that no PDF file was left behind
    assert not (tmp_path / "Rplots.pdf").exists()


def test_cube_visualization(local_cube):
    """Test cube visualization."""
    # Plot the result
    assert_is_figure(sits_plot(local_cube))


def test_classified_cube_visualization():
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
    assert_is_figure(sits_plot(cube))


def test_sits_visualization_leaflet(no_browser):
    """Test sits visualization."""
    sits_view(samples_l8_rondonia_2bands)


def test_cube_visualization_leaflet(local_cube, no_browser):
    """Test cube visualization."""
    sits_view(local_cube)


def test_sankey_visualization(class_cubes):
    """Test sankey visualization of class trajectories."""
    class_2013, class_2014 = class_cubes

    assert_is_figure(
        sits_sankey(
            class_2013,
            class_2014,
            labels=["2013", "2014"],
            multicores=1,
            progress=False,
        )
    )


def test_sankey_visualization_cubes_argument(class_cubes):
    """Test sankey visualization using the ``cubes`` argument."""
    class_2013, class_2014 = class_cubes

    # Cubes can also be given as a list, instead of separate arguments
    assert_is_figure(
        sits_sankey(
            cubes=[class_2013, class_2014],
            labels=["2013", "2014"],
            title="Trajectories",
            palette="Set2",
            multicores=1,
            progress=False,
        )
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


#
# Multiple figures
#
def test_visualization_multiple_figures():
    """Test samples that produce one figure per label."""
    plots = sits_plot(cerrado_2classes[:5])

    # Check type and length
    assert isinstance(plots, SITSPlotList)
    assert len(plots) == 2  # noqa: PLR2004

    # Check all figures
    for plot in plots:
        assert_is_figure(plot)

    # Every figure is available to HTML front-ends
    assert plots.to_html().count("data:image/png;base64,") == len(plots)

    # Get representation values
    payload, metadata = plots._repr_png_()
    width, height = plots.options.display_size

    # Check representation
    assert payload.startswith(PNG_SIGNATURE)
    assert metadata == {"width": width, "height": height * len(plots)}


def test_visualization_multiple_figures_indexing():
    """Test selecting figures out of a multi-figure result."""
    # Plot the result
    plots = sits_plot(cerrado_2classes[:5])

    # Check type
    assert isinstance(plots[0], SITSPlot)
    assert isinstance(plots[0:1], SITSPlotList)

    # Check contents
    assert list(plots) == [plots[0], plots[1]]


#
# Plot options
#
def test_visualization_image_args():
    """Test that per-call plot options reach the R device."""
    # Plot the result
    plot = sits_plot(
        point_mt_6bands,
        image_args={
            "width": 4,
            "height": 3,
            "res": 100,
        },
    )

    # Check that the figure is valid
    assert_is_figure(plot)

    # Check size and DPI
    assert plot.size == (400, 300)
    assert plot.dpi == 100  # noqa: PLR2004


def test_visualization_image_args_unknown_key():
    """Test that a mistyped plot option is reported."""
    with pytest.raises(ValueError, match="Unknown image_args: resolution"):
        sits_plot(point_mt_6bands, image_args={"resolution": 100})


def test_visualization_host_options():
    """Test that the plot options declared by the host document are honoured.

    Quarto writes the document `fig-width`, `fig-height`, and `fig-dpi`
    options into `matplotlib.rcParams` when it starts the kernel, which
    is how a document configures its figures.
    """
    # Set figure size and DPI
    matplotlib.rcParams["figure.figsize"] = (7, 5)
    matplotlib.rcParams["figure.dpi"] = 96

    # Plot the result
    plot = sits_plot(point_mt_6bands)

    # Check size and DPI
    assert plot.size == (672, 480)

    # Check representation
    assert plot._repr_png_()[1] == {"width": 672, "height": 480}


def test_visualization_options_precedence():
    """Test that explicit plot options win over the host document."""
    matplotlib.rcParams["figure.figsize"] = (7, 5)
    matplotlib.rcParams["figure.dpi"] = 96

    # Set DPI
    set_plot_options(dpi=120)

    # Check size
    assert sits_plot(point_mt_6bands).size == (840, 600)

    # Plot the result
    plot = sits_plot(point_mt_6bands, image_args={"res": 50})

    # Check size
    assert plot.size == (350, 250)


#
# Output files
#
def test_visualization_save(tmp_path: Path):
    """Test writing a figure to disk."""
    # Plot the result
    plot = sits_plot(point_mt_6bands, image_args={"res": 100})

    # Check path
    path = plot.save(tmp_path / "figure.png")

    assert path.read_bytes() == plot.data
    assert Image.open(path).size == plot.size

    # Get converted figure
    converted = plot.save(tmp_path / "figure.jpeg")

    # Check that the format is converted
    assert Image.open(converted).format == "JPEG"


def test_visualization_save_multiple(tmp_path: Path):
    """Test writing a multi-figure result to disk."""
    plots = sits_plot(cerrado_2classes[:5], image_args={"res": 100})

    # Plot the result
    paths = plots.save(tmp_path / "figure.png")

    # Check paths
    assert [path.name for path in paths] == ["figure_1.png", "figure_2.png"]
    assert all(path.exists() for path in paths)


#
# Failure handling
#
def test_visualization_error_closes_device(local_cube, tmp_path, monkeypatch):
    """Test that a failing plot method leaves no device open."""
    # Change working directory
    monkeypatch.chdir(tmp_path)

    # Plot the result
    with pytest.raises(RRuntimeError):
        sits_plot(local_cube, band="NOT_A_BAND")

    # Check that no PDF file was left behind
    assert not (tmp_path / "Rplots.pdf").exists()


def test_visualization_error_while_rendering_closes_device(monkeypatch):
    """Test that a failure while drawing leaves no device open."""

    # Set failing print function
    def failing_print(*args, **kwargs):
        raise RRuntimeError("drawing failed")

    monkeypatch.setattr(base, "r_fnc_print", failing_print)

    # Plot the result
    with pytest.raises(RRuntimeError, match="drawing failed"):
        sits_plot(point_mt_6bands)
