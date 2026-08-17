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

"""Base visualization utilities."""

import tempfile
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any

from pysits.backend.functions import r_fnc_plot, r_fnc_print
from pysits.models.visual import ImageArgs, PlotOptions, SITSPlot, SITSPlotList
from pysits.visualization.device import null_device, png_device
from pysits.visualization.host import display_figures
from pysits.visualization.options import resolve_plot_options

#
# Constants
#
GRAPHICS_CLASSES = {
    "ggplot",
    "ggplot2::ggplot",
    "gg",
    "tmap",
    "patchwork",
    "gtable",
    "grob",
    "trellis",
    "recordedplot",
}
"""R classes of objects that draw themselves when printed."""

GRAPHICS_CLASS_WRAPPER = {"list"}
"""R class of a graphics object wrapper."""


#
# Utility functions
#
def _flatten_figures(obj: Any) -> list[Any]:
    """Collect the drawable figures returned by an R plot method.

    Args:
        obj (Any): The value returned by the R plot method.

    Returns:
        list[Any]: The figures found, in order. Empty when the method drew on
              the device instead of returning something drawable.
    """
    # `rclass` is an R character vector, not a Python set
    classes = frozenset(getattr(obj, "rclass", ()))

    if classes & GRAPHICS_CLASSES:
        return [obj]

    if classes == GRAPHICS_CLASS_WRAPPER:
        return [figure for item in obj for figure in _flatten_figures(item)]

    return []


def _render(draw: Callable[[], Any], path: Path, options: PlotOptions) -> bytes:
    """Render a figure.

    Args:
        draw (Callable): Callable that draws on the active device.

        path (pathlib.Path): File the device writes to.

        options (PlotOptions): Geometry to render with.

    Returns:
        bytes: The rendered PNG.

    Raises:
        RuntimeError: If the device produced no image.
    """
    with png_device(path, options):
        draw()

    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(
            "R produced no image for this object. This usually means the "
            "plot method drew nothing for the arguments it was given."
        )

    return path.read_bytes()


#
# High-level operation
#
def plot_base(
    instance: Any,
    image_args: ImageArgs | None = None,
    **kwargs: Any,
) -> SITSPlot | SITSPlotList:
    """Render an R object as one or more figures.

    The object is plotted twice on purpose. The first call, on a device
    that discards its output, is what reveals how the plot method behaves:
    methods that build a graphics object return it, and methods that draw
    as a side effect return their input. The figures are then drawn on a
    PNG device - either by printing the graphics objects, or by running the
    plot method again for the methods that only draw.

    Args:
        instance: The R object to be plotted.

        image_args (dict): Image configuration, with any of the keys
                           ``width`` and ``height`` (in inches), and
                           ``res`` (in dots per inch). Defaults come from
                           the host document and from
                           ``set_plot_options``.

        **kwargs: Additional keyword arguments passed to R's ``plot``.

    Returns:
        SITSPlot | SITSPlotList: The rendered figure, or every figure the
                                 plot method produced.
    """
    options = resolve_plot_options(image_args)

    # Discover what the plot method does, using null device to avoid
    # the creation of any output files.
    with null_device():
        result = r_fnc_plot(instance, **kwargs)

    # Flatten the result into a list of figures
    figures = _flatten_figures(result)

    # Render the figures on a PNG device. For this
    # creates a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        # If the plot method drew nothing, render the
        # instance again
        if not figures:
            # Render the instance again, this time on a PNG device
            payload = _render(
                partial(r_fnc_plot, instance, **kwargs),
                directory / "plot.png",
                options,
            )

            # Create the plot object
            plot = SITSPlot(result, payload, options)

        # Otherwise, there are figures to render
        else:
            # Render the figures on a PNG device
            plots = [
                SITSPlot(
                    figure,
                    _render(
                        partial(r_fnc_print, figure),
                        directory / f"plot_{index}.png",
                        options,
                    ),
                    options,
                )
                for index, figure in enumerate(figures)
            ]

            # Create the plot object
            plot = plots[0] if len(plots) == 1 else SITSPlotList(result, plots)

    # Hosts that collect figures through `pyplot` / `knitr`, and so RStudio
    # chunks, are handed the figures here. Everywhere else, this does nothing.
    display_figures(plot)

    # Return!
    return plot
