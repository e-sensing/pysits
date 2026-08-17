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

"""R graphics device management."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from rpy2.robjects import NULL as R_NULL

from pysits.backend.pkgs import r_pkg_grdevices
from pysits.models.visual import PlotOptions


#
# Context managers
#
@contextmanager
def null_device() -> Iterator[None]:
    """Run R code with a device that discards everything drawn on it.

    Some ``sits`` plot methods draw as a side effect instead of returning a
    graphics object. Calling them with no device open makes R fall back to
    its default device, which writes an ``Rplots.pdf`` file into the
    working directory and stays open. Wrapping the call in this device
    keeps that output where it belongs: nowhere.

    Yields:
        None: Nothing.
    """
    # `pdf(NULL)` is R null device, which produces no file at all
    r_pkg_grdevices.pdf(file=R_NULL)

    try:
        yield

    finally:
        r_pkg_grdevices.dev_off()


@contextmanager
def png_device(path: Path, options: PlotOptions) -> Iterator[None]:
    """Run R code with a PNG device open.

    The device is closed even when the enclosed code fails, so a plotting
    error cannot leave it open in the R session.

    Args:
        path (pathlib.Path): File the device writes to.

        options (PlotOptions): Geometry to render with.

    Yields:
        None: Nothing.
    """
    # Get dimensions
    width, height = options.pixel_size

    # Open the device
    r_pkg_grdevices.png(
        file=str(path),
        width=width,
        height=height,
        res=options.dpi,
    )

    try:
        yield

    finally:
        r_pkg_grdevices.dev_off()
