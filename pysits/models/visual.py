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

"""Visual models."""

import base64
import sys
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Any, TypeAlias

from matplotlib.figure import Figure as MatplotlibFigure
from PIL import Image as PILImage

from pysits.models.base import SITSBase

#
# Type aliases
#
FilePath: TypeAlias = str | PathLike[str]
ImageArgs: TypeAlias = dict[str, int | float]


#
# Constants
#
CSS_DPI = 96
"""CSS reference pixels per inch.

A CSS pixel is defined as 1/96 of an inch. Converting the figure size with
this factor, instead of the rendering resolution, is what keeps a
high-resolution figure from being displayed at an enormous on-screen size:
the payload stays crisp, while the layout follows the physical size the
figure was drawn at.
"""

DISPLAY_HOOK_MODULES = ("rpytools",)
"""Modules a host installs its ``pyplot.show`` capture hook from.

``rpytools`` is the Python side of ``reticulate``, which is what runs
Python chunks in RStudio and in Quarto documents using the ``knitr``
engine. It replaces ``matplotlib.pyplot.show`` with a hook that writes the
current figure to the document's figure directory.
"""

NO_ALPHA_EXTENSIONS_SUFFIXES = (".jpg", ".jpeg")
"""File extensions that require dropping the alpha channel before saving."""


#
# Host detection
#
def display_hook_installed() -> bool:
    """Check whether the host captures figures through ``pyplot``.

    Front-ends differ in how they take a figure from Python. Notebooks read
    the rich-display methods, while ``knitr`` only learns about a figure
    when ``pyplot.show`` is called. It patches that function to intercept
    the call. Detecting the patch is what tells the two apart.

    Returns:
        bool: ``True`` when a figure-capture hook is installed.
    """
    pyplot = sys.modules.get("matplotlib.pyplot")

    if pyplot is None:
        return False

    origin = getattr(pyplot.show, "__module__", "") or ""

    return origin.startswith(DISPLAY_HOOK_MODULES)


#
# Utility functions
#
def _encode_data_uri(data: bytes) -> str:
    """Encode PNG bytes as a ``data:`` URI.

    Args:
        data (bytes): PNG payload.

    Returns:
        str: The payload as an inline ``data:image/png;base64`` URI.
    """
    return f"data:image/png;base64,{base64.b64encode(data).decode('ascii')}"


def _stack_images(images: Sequence[PILImage.Image]) -> PILImage.Image:
    """Stack images vertically on a single canvas.

    Images narrower than the widest one are centred horizontally.

    Args:
        images (Sequence[PIL.Image.Image]): Images to stack, top to bottom.

    Returns:
        PIL.Image.Image: The combined image.
    """
    width = max(image.width for image in images)
    height = sum(image.height for image in images)

    canvas = PILImage.new("RGB", (width, height), color="white")

    offset = 0
    for image in images:
        canvas.paste(image, ((width - image.width) // 2, offset))
        offset += image.height

    return canvas


#
# Rendering options
#
@dataclass(frozen=True)
class PlotOptions:
    """Geometry used to render a figure."""

    width: float = 10.0
    """Figure width, in inches."""

    height: float = 6.0
    """Figure height, in inches."""

    dpi: int = 300
    """Rendering resolution, in dots per inch."""

    #
    # Internal methods
    #
    def __post_init__(self) -> None:
        """Validate the geometry."""
        for name in ("width", "height", "dpi"):
            value = getattr(self, name)

            if value <= 0:
                raise ValueError(f"Plot `{name}` must be positive (got {value!r}).")

    #
    # Properties
    #
    @property
    def pixel_size(self) -> tuple[int, int]:
        """Size of the rendered image, in pixels."""
        return (
            round(self.width * self.dpi),
            round(self.height * self.dpi),
        )

    @property
    def display_size(self) -> tuple[int, int]:
        """Size the image should be displayed at, in CSS pixels."""
        return (
            round(self.width * CSS_DPI),
            round(self.height * CSS_DPI),
        )


#
# Plot models
#
class SITSPlot(SITSBase):
    """A single figure rendered from an R graphics object.

    The figure is held as a PNG payload and exposed through the standard
    IPython rich-display protocol, so notebooks, Quarto, and any other
    front-end that understands ``image/png`` render it as a real figure.
    """

    #
    # Internal methods
    #
    def __init__(self, instance: Any, data: bytes, options: PlotOptions) -> None:
        """Initializer.

        Args:
            instance (Any): The R graphics object the figure was rendered from.

            data (bytes): PNG payload.

            options (PlotOptions): Geometry used to render the figure.
        """
        super().__init__(instance)

        self._data = data
        self._options = options
        self._size = PILImage.open(BytesIO(data)).size

    def __repr__(self) -> str:
        """Representation.

        Empty when the host captures figures through ``pyplot``: the figure
        has already been handed over, and printing a description of it next
        to the figure itself is noise.
        """
        if display_hook_installed():
            return ""

        width, height = self._size

        return f"<SITSPlot {width}x{height}px @ {self._options.dpi}dpi>"

    #
    # Properties
    #
    @property
    def data(self) -> bytes:
        """PNG payload of the figure."""
        return self._data

    @property
    def options(self) -> PlotOptions:
        """Geometry used to render the figure."""
        return self._options

    @property
    def size(self) -> tuple[int, int]:
        """Size of the rendered figure, in pixels."""
        return self._size

    @property
    def dpi(self) -> int:
        """Resolution the figure was rendered at, in dots per inch."""
        return self._options.dpi

    #
    # Representation
    #
    def _repr_png_(self) -> tuple[bytes, dict[str, int]]:
        """Rich display as a PNG image, sized by the figure geometry."""
        width, height = self._options.display_size

        dimensions = {
            "width": width,
            "height": height,
        }

        return self._data, dimensions

    #
    # Data management
    #
    def to_matplotlib(self, figure: MatplotlibFigure | None = None) -> MatplotlibFigure:
        """Draw the figure onto a matplotlib figure.

        The image is drawn on axes covering the whole canvas, so the result
        carries no margins, ticks, or frame of its own. The figure keeps
        exactly the appearance R gave it.

        Args:
            figure (matplotlib.figure.Figure): Figure to draw on. A new one,
                                               sized to match, is created
                                               when omitted.

        Returns:
            matplotlib.figure.Figure: The figure drawn on.
        """
        if figure is None:
            figure = MatplotlibFigure(
                figsize=(self._options.width, self._options.height),
                dpi=self._options.dpi,
            )

        axes = figure.add_axes((0, 0, 1, 1))
        axes.set_axis_off()

        # Left at the default interpolation: it resamples only when the
        # figure is written at a resolution other than the rendered one
        axes.imshow(self.to_pil())

        return figure

    def to_pil(self) -> PILImage.Image:
        """Convert the figure to a Pillow image.

        Returns:
            PIL.Image.Image: The decoded figure.
        """
        return PILImage.open(BytesIO(self._data))

    def save(self, path: FilePath) -> Path:
        """Write the figure to a file.

        The image is written as-is when the target is a PNG. Any other
        extension is converted with Pillow.

        Args:
            path (str | os.PathLike): Destination file. A missing extension
                                      is assumed to be ``.png``.

        Returns:
            pathlib.Path: The path written to.
        """
        path = Path(path)

        # If there is no extension, assume PNG as default
        if not path.suffix:
            path = path.with_suffix(".png")

        # If the extension is PNG, no extra conversion is needed
        if path.suffix.lower() == ".png":
            # Save it
            path.write_bytes(self._data)

            # Return!
            return path

        # Otherwise, first convert to pillow image
        image = self.to_pil()

        # If required, remove alpha channel
        if path.suffix.lower() in NO_ALPHA_EXTENSIONS_SUFFIXES:
            image = image.convert("RGB")

        # Save the image
        image.save(path)

        # Return!
        return path

    def show(self) -> None:
        """Open the figure in the default image viewer.

        Plotting does not display anything by itself: in a notebook the
        figure is rendered as the cell result, and in a script this is how
        it is shown.

        Returns:
            None: Nothing.
        """
        self.to_pil().show()


class SITSPlotList(SITSBase, Sequence[SITSPlot]):
    """Several figures produced by a single plot call.

    Rendered as a gallery where HTML is supported, and as a single stacked
    image everywhere else (for example, when Quarto targets PDF), so the
    figures survive every output format.
    """

    #
    # Internal methods
    #
    def __init__(self, instance: Any, plots: Sequence[SITSPlot]) -> None:
        """Initializer.

        Args:
            instance (Any): The R graphics object the figures were rendered from.

            plots (Sequence[SITSPlot]): The rendered figures, in order.

        Raises:
            ValueError: If ``plots`` is empty.
        """
        if not plots:
            raise ValueError("A plot list requires at least one figure.")

        super().__init__(instance)

        self._plots = tuple(plots)
        self._composite: bytes | None = None

    def __repr__(self) -> str:
        """Representation."""
        if display_hook_installed():
            return ""

        # Total number of figures
        total = len(self._plots)

        # Return!
        return f"<SITSPlotList of {total} figure{'s' if total > 1 else ''}>"

    def __len__(self) -> int:
        """Number of figures."""
        return len(self._plots)

    def __iter__(self) -> Iterator[SITSPlot]:
        """Iterate over the figures."""
        return iter(self._plots)

    def __getitem__(self, index: int | slice) -> "SITSPlot | SITSPlotList":
        """Select figures by position."""
        if isinstance(index, slice):
            return SITSPlotList(
                instance=self._instance,
                plots=self._plots[index],
            )

        return self._plots[index]

    #
    # Properties
    #
    @property
    def options(self) -> PlotOptions:
        """Geometry used to render the figures."""
        return self._plots[0].options

    #
    # Representation
    #
    def _repr_mimebundle_(
        self,
        include: object = None,
        exclude: object = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Rich display as a gallery, with an image for other front-ends."""
        # Get the PNG payload and metadata
        payload, metadata = self._repr_png_()

        # Create the data bundle
        data = {
            "text/html": self.to_html(),
            "image/png": payload,
        }

        # Image metadata
        image_metadata = {
            "image/png": metadata,
        }

        # Return!
        return data, image_metadata

    def _repr_png_(self) -> tuple[bytes, dict[str, int]]:
        """Rich display as a single stacked image.

        Used by front-ends that cannot render HTML. This is the case
        of Quarto when it targets a non-HTML format.
        """
        # Get image dimensions
        width, height = self.options.display_size

        # Define dimensions
        dimensions = {
            "width": width,
            "height": height * len(self._plots),
        }

        # Return!
        return self.to_png(), dimensions

    #
    # Data management
    #
    def to_matplotlib(self) -> list[MatplotlibFigure]:
        """Draw the figures onto matplotlib figures, one each.

        Returns:
            list[matplotlib.figure.Figure]: The figures, in order.
        """
        return [plot.to_matplotlib() for plot in self._plots]

    def to_html(self) -> str:
        """Render the figures as an HTML gallery.

        Returns:
            str: A gallery of inline images, one per figure.
        """
        from pysits.jinja import get_template

        # Get image dimendions
        width, height = self.options.display_size

        # Number of plots
        total = len(self._plots)

        # Generate figures metadata
        figures = [
            {
                "source": _encode_data_uri(plot.data),
                "width": width,
                "height": height,
                "alt": f"Figure {index} of {total}",
            }
            for index, plot in enumerate(self._plots, start=1)
        ]

        # Render!
        return get_template("plot.html").render(figures=figures)

    def to_pil(self) -> PILImage.Image:
        """Combine the figures into a single Pillow image.

        Returns:
            PIL.Image.Image: The figures stacked vertically.
        """
        return _stack_images([plot.to_pil() for plot in self._plots])

    def to_png(self) -> bytes:
        """Combine the figures into a single PNG payload.

        Returns:
            bytes: The figures stacked vertically, encoded as PNG.
        """
        if self._composite is None:
            # Create a buffer to store the image
            buffer = BytesIO()

            # Save the image
            self.to_pil().save(buffer, format="PNG")

            # Store the image
            self._composite = buffer.getvalue()

        # Return!
        return self._composite

    def save(self, path: FilePath) -> list[Path]:
        """Write the figures to files, one per figure.

        Each figure is written next to the given path, with its position
        appended to the file name (``plot.png`` becomes ``plot_1.png``,
        ``plot_2.png``, ...).

        Args:
            path (str | os.PathLike): Destination file. A missing extension
                                      is assumed to be ``.png``.

        Returns:
            list[pathlib.Path]: The paths written to, in figure order.
        """
        path = Path(path)

        if not path.suffix:
            path = path.with_suffix(".png")

        # Save each plot
        paths = []

        for index, plot in enumerate(self._plots, start=1):
            paths.append(
                plot.save(
                    path=path.with_name(f"{path.stem}_{index}{path.suffix}"),
                ),
            )

        # Return!
        return paths

    def show(self) -> None:
        """Open the stacked figures in the default image viewer.

        Returns:
            None: Nothing.
        """
        self.to_pil().show()
