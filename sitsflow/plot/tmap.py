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

"""tmap plot module."""

import os
import tempfile

from IPython.display import display
from PIL import Image
from rpy2.robjects import r

from sitsflow.backend.utils import r_plot


def save_tmap_plot(
    r_tmap_plot, filename="tmap_plot.png", width=1024, height=1024, fmt="png"
):
    """Saves an R tmap plot to a temporary directory and displays it.

    Args:
        r_tmap_plot (rpy2.robjects.RObject): The R tmap plot object.

        filename (str): The name of the output file (default: ``tmap_plot.png``).

        width (int): Width of the saved image (default: 1024).

        height (int): Height of the saved image (default: 1024).

        fmt (str): Image format (default: ``png``). Options: ``png``,
                   ``jpeg``, or ``tiff``.

    Returns:
        str: Path to the saved image.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, f"tmap_plot.{fmt}")

    # Ensure the format is supported
    valid_formats = ["png", "jpeg", "tiff"]
    if fmt not in valid_formats:
        raise ValueError(f"Unsupported format: {fmt}. Choose from {valid_formats}.")

    # Save the tmap plot using R
    r("tmap::tmap_save")(r_tmap_plot, filename=file_path, width=width, height=height)

    # Display the saved image
    display(Image.open(file_path))

    return file_path


def plot_tmap(
    instance, filename="tmap_plot.png", width=1024, height=1024, fmt="png", **kwargs
):
    """Generates and saves a tmap plot, then displays it.

    Args:
        instance (rpy2.robjects.RObject): The R object instance for plotting.

        filename (str): Name of the output file (default: "tmap_plot.png").

        width (int): Width of the saved image (default: 1024).

        height (int): Height of the saved image (default: 1024).

        fmt (str): Image format (default: ``png``). Options: ``png``,
                   ``jpeg``, or ``tiff``.

        **kwargs: Additional keyword arguments for the R plotting function.

    Returns:
        str: Path to the saved image.
    """
    # Generate the R plot
    tmap_plot = r_plot(instance, **kwargs)

    # Save and display the plot
    return save_tmap_plot(
        tmap_plot, filename=filename, width=width, height=height, fmt=fmt
    )
