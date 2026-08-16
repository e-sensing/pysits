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

"""Unit tests for plot models and rendering options."""

from io import BytesIO
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest
from IPython.core.formatters import DisplayFormatter
from matplotlib.figure import Figure
from PIL import Image

from pysits.models.visual import (
    PlotOptions,
    SITSPlot,
    SITSPlotList,
    display_hook_installed,
)
from pysits.visualization.host import display_figures
from pysits.visualization.options import (
    get_plot_options,
    reset_plot_options,
    resolve_plot_options,
    set_plot_options,
)


#
# Helpers
#
def make_png(width: int, height: int, color: str = "white") -> bytes:
    """Build a PNG payload of a given size."""
    # Create buffer
    buffer = BytesIO()

    # Create image and save to buffer
    Image.new("RGB", (width, height), color=color).save(buffer, format="PNG")

    # Return!
    return buffer.getvalue()


def make_plot(width: float = 10.0, height: float = 6.0, dpi: int = 100) -> SITSPlot:
    """Build a figure matching the given options."""
    # Create options
    options = PlotOptions(
        width=width,
        height=height,
        dpi=dpi,
    )

    # Create plot
    return SITSPlot(
        None,
        make_png(*options.pixel_size),
        options,
    )


def install_hook(monkeypatch, show) -> None:
    """Replace `pyplot.show` with a host hook."""
    # Set module
    show.__module__ = "rpytools.call"

    # Set hook
    monkeypatch.setattr(plt, "show", show)


#
# Fixtures
#
@pytest.fixture
def hosted_pyplot(monkeypatch):
    """Simulate a host that captures figures through ``pyplot``.

    Mirrors what ``reticulate`` does: it replaces ``pyplot.show`` with a
    hook that writes the current figure out and closes it.

    Yields:
        list: The figures handed over, in order.
    """
    captured = []

    def show(*args, **kwargs):
        captured.append(plt.gcf())
        plt.close()

    # Install hook
    install_hook(monkeypatch, show)

    # Yield captured figures
    yield captured

    # Close all figures
    plt.close("all")


#
# Rendering options
#
def test_plot_options():
    """Test the sizes derived from the figure options."""
    # Create options
    options = PlotOptions(
        width=10,
        height=6,
        dpi=300,
    )

    # Check that the figure is rendered at the requested resolution
    assert options.pixel_size == (3000, 1800)

    # Check that the figure is displayed at the physical size, in CSS pixels
    assert options.display_size == (960, 576)

    # Check that invalid options are rejected
    for field in ("width", "height", "dpi"):
        with pytest.raises(ValueError, match=f"Plot `{field}` must be positive"):
            PlotOptions(**{field: 0})


def test_plot_options_sources():
    """Test where the plot options are read from.

    A host declares its figure options through `matplotlib.rcParams`,
    which is what Quarto writes its `fig-width`, `fig-height`, and
    `fig-dpi` options into.
    """
    # Check that the default options are used
    assert resolve_plot_options() == PlotOptions(
        width=10.0,
        height=6.0,
        dpi=300,
    )

    # Set figure size and DPI
    matplotlib.rcParams["figure.figsize"] = (7, 5)
    matplotlib.rcParams["figure.dpi"] = 96

    # Check that the options are read from the host
    assert resolve_plot_options() == PlotOptions(
        width=7.0,
        height=5.0,
        dpi=96,
    )

    # Reset matplotlib defaults
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)

    # Check that the default options are used
    assert resolve_plot_options() == PlotOptions()


def test_plot_options_precedence():
    """Test the order the plot options sources are applied in."""
    matplotlib.rcParams["figure.figsize"] = (7, 5)
    matplotlib.rcParams["figure.dpi"] = 96

    # Set DPI
    set_plot_options(dpi=150)

    # Check that the DPI is set
    assert resolve_plot_options() == PlotOptions(
        width=7.0,
        height=5.0,
        dpi=150,
    )

    # Set width and DPI
    assert resolve_plot_options({"width": 4, "res": 50}) == PlotOptions(4, 5.0, 50)

    # Reset plot options
    assert reset_plot_options() == PlotOptions(width=7.0, height=5.0, dpi=96)


def test_plot_options_rejects_invalid_values():
    """Test that invalid plot options are rejected."""
    with pytest.raises(ValueError, match="Unknown image_args: nope, resolution"):
        resolve_plot_options({"resolution": 100, "nope": 1})

    # Check that invalid plot options are rejected
    with pytest.raises(ValueError, match="must be positive"):
        set_plot_options(dpi=-1)

    # Check that the default options are used
    assert get_plot_options() == PlotOptions()


#
# Single figure
#
def test_plot_attributes():
    """Test the figure attributes and its textual representation."""
    plot = make_plot(
        width=4,
        height=3,
        dpi=100,
    )

    # Check plot attributes
    assert plot.size == (400, 300)
    assert plot.dpi == 100  # noqa: PLR2004
    assert plot.options == PlotOptions(width=4, height=3, dpi=100)
    assert plot.to_pil().size == (400, 300)
    assert repr(plot) == "<SITSPlot 400x300px @ 100dpi>"


def test_plot_repr_png():
    """Test the rich display payload and its display options."""
    # Create plot
    plot = make_plot(
        width=4,
        height=3,
        dpi=300,
    )
    payload, metadata = plot._repr_png_()

    # Check payload
    assert payload is plot.data

    # Check size and metadata
    assert plot.size == (1200, 900)
    assert metadata == {"width": 384, "height": 288}


def test_plot_save(tmp_path: Path):
    """Test writing a figure to disk, in each supported format."""
    plot = make_plot(
        width=4,
        height=3,
        dpi=100,
    )

    # Create plot
    assert plot.save(tmp_path / "figure.png").read_bytes() == plot.data

    # Check that a missing extension is assumed to be PNG
    path = plot.save(tmp_path / "figure")

    # Check path
    assert path.name == "figure.png"
    assert Image.open(path).format == "PNG"

    # Any other extension is converted on the way out
    assert Image.open(plot.save(tmp_path / "figure.jpeg")).format == "JPEG"


#
# Multiple figures
#
def test_plot_list_sequence():
    """Test the sequence interface."""
    plots = [make_plot(), make_plot()]
    plot_list = SITSPlotList(None, plots)

    # Check length and sequence
    assert len(plot_list) == 2  # noqa: PLR2004
    assert list(plot_list) == plots
    assert plot_list[1] is plots[1]
    assert repr(plot_list) == "<SITSPlotList of 2 figures>"

    # Check slicing
    sliced = plot_list[:1]

    # Check type
    assert isinstance(sliced, SITSPlotList)
    assert repr(sliced) == "<SITSPlotList of 1 figure>"

    # Check that an empty list is rejected
    with pytest.raises(ValueError, match="at least one figure"):
        SITSPlotList(None, [])


def test_plot_list_composite():
    """Test the stacked image rendered for HTML front-ends."""
    # Create plot list
    plot_list = SITSPlotList(
        instance=None, plots=[make_plot(width=4, height=3, dpi=100)] * 2
    )

    payload, metadata = plot_list._repr_png_()

    # Check size and metadata
    assert Image.open(BytesIO(payload)).size == (400, 600)
    assert metadata == {"width": 384, "height": 576}

    # Check that the plot list is built once, then reused
    assert plot_list.to_png() is plot_list.to_png()

    # Check that figures of different widths share a common canvas
    uneven = SITSPlotList(
        None,
        [
            make_plot(width=4, height=3, dpi=100),
            make_plot(width=6, height=3, dpi=100),
        ],
    )

    # Check size
    assert uneven.to_pil().size == (600, 600)


def test_plot_list_gallery():
    """Test the gallery rendered for HTML front-ends."""
    # Create plot list
    plot_list = SITSPlotList(
        instance=None,
        plots=[make_plot(), make_plot()],
    )

    # Get HTML representation
    html = plot_list.to_html()

    # Check that every figure is embedded
    assert html.count("data:image/png;base64,") == 2  # noqa: PLR2004

    width, height = plot_list.options.display_size

    # Check width and height
    assert f'width="{width}"' in html
    assert f'height="{height}"' in html


def test_plot_list_save(tmp_path: Path):
    """Test writing every figure to disk."""
    # Create plot list
    plot_list = SITSPlotList(
        instance=None,
        plots=[make_plot(), make_plot()],
    )

    # Save plot list
    paths = plot_list.save(tmp_path / "figure.png")

    # Check paths
    assert [path.name for path in paths] == ["figure_1.png", "figure_2.png"]
    assert all(path.exists() for path in paths)

    # Check that a missing extension is assumed to be PNG
    paths = plot_list.save(tmp_path / "plain")

    assert [path.name for path in paths] == ["plain_1.png", "plain_2.png"]


#
# Matplotlib bridge
#
def test_to_matplotlib():
    """Test the matplotlib figure built from a plot."""
    # Create plot
    plot = make_plot(
        width=8,
        height=5,
        dpi=150,
    )

    # Convert to matplotlib figure
    figure = plot.to_matplotlib()

    # Check size and DPI
    assert tuple(figure.get_size_inches()) == (8, 5)
    assert figure.dpi == 150  # noqa: PLR2004

    # Check that the image covers the whole canvas
    (axes,) = figure.axes

    # Check image properties
    assert axes.get_position().bounds == (0, 0, 1, 1)
    assert not axes.axison

    # Write figure to buffer
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=figure.dpi)

    # Check that the figure is pixel-identical to what R drew
    assert Image.open(buffer).size == plot.options.pixel_size

    # Check that converting leaves the pyplot state machine free
    assert plt.get_fignums() == []


def test_to_matplotlib_targets():
    """Test drawing onto a given figure, and converting a whole list."""
    # Create target figure
    target = Figure()

    # Check figure and axes
    assert make_plot().to_matplotlib(target) is target
    assert len(target.axes) == 1

    # Convert plot list to matplotlib figures
    figures = SITSPlotList(
        instance=None,
        plots=[make_plot(), make_plot()],
    ).to_matplotlib()

    # Check length and axes
    assert len(figures) == 2  # noqa: PLR2004
    assert all(len(figure.axes) == 1 for figure in figures)


#
# Host handover
#
def test_display_hook_detection(monkeypatch):
    """Test that a host capture hook is told apart from an ordinary session."""

    def show(*args, **kwargs):
        """Stand in for the hook a host installs."""

    # Check that no hook is installed
    assert not display_hook_installed()

    # Install hook
    install_hook(monkeypatch, show)

    # Check that the hook is installed
    assert display_hook_installed()


def test_display_figures(hosted_pyplot):
    """Test that figures are handed over one at a time."""
    # Create plot
    display_figures(make_plot(width=8, height=5, dpi=150))

    # Check figure
    (figure,) = hosted_pyplot

    # Check size and DPI
    assert tuple(figure.get_size_inches()) == (8, 5)
    assert figure.dpi == 150  # noqa: PLR2004

    # Check that the figure is closed
    hosted_pyplot.clear()

    # Display plot list
    display_figures(
        plot=SITSPlotList(
            instance=None,
            plots=[make_plot()] * 3,
        ),
    )

    # Check length
    assert len(hosted_pyplot) == 3  # noqa: PLR2004


def test_display_figures_leaves_no_open_figure(monkeypatch):
    """Test that figures never pile up in the pyplot state machine."""

    def show(*args, **kwargs):
        """A host that takes the figure but never closes it."""

    # Check that nothing is shown when no host is listening
    display_figures(make_plot())

    # Check that no figures are open
    assert plt.get_fignums() == []

    # Install hook
    install_hook(monkeypatch, show)

    # Display plot list
    display_figures(SITSPlotList(instance=None, plots=[make_plot(), make_plot()]))

    # Check that no figures are open
    assert plt.get_fignums() == []


#
# Representation
#
def test_representation_under_a_host(hosted_pyplot):
    """Test that nothing is written beside the figures a host collected."""
    for plot in (make_plot(), SITSPlotList(instance=None, plots=[make_plot()])):
        assert repr(plot) == ""
        assert not hasattr(plot, "_repr_html_")
        assert not hasattr(plot, "_repr_markdown_")

    # Check that the image representation keeps working
    payload, metadata = make_plot()._repr_png_()

    # Check payload
    assert payload.startswith(b"\x89PNG\r\n\x1a\n")

    # Check size and metadata
    assert metadata == {"width": 960, "height": 576}


def test_representation_bundle():
    """Test the representations a notebook front-end receives."""
    # Create plot list
    plots = SITSPlotList(instance=None, plots=[make_plot(), make_plot()])

    # Check MIME bundle
    data, metadata = plots._repr_mimebundle_()

    assert data["text/html"].count("data:image/png;base64,") == 2  # noqa: PLR2004
    assert data["image/png"] == plots.to_png()
    assert metadata["image/png"] == {"width": 960, "height": 1152}

    # Check that IPython assembles the bundle the front-end sees
    data, metadata = DisplayFormatter().format(
        SITSPlotList(instance=None, plots=[make_plot()]),
    )

    # Check data
    assert sorted(data) == ["image/png", "text/html", "text/plain"]

    # Check size and metadata
    assert metadata["image/png"] == {"width": 960, "height": 576}
