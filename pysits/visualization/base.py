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

import os
import tempfile
from typing import Any, TypeAlias

from pysits.backend.functions import r_fnc_plot
from pysits.backend.pkgs import r_pkg_grdevices
from pysits.visualization.image import show_local_image

#
# Type aliases
#
ImageArgs: TypeAlias = dict[str, int | float]


#
# Utility function
#
def _base_plot(data: Any, image_args: ImageArgs | None = None, **kwargs: Any) -> str:
    """Save and show images created using base plot.

    This function creates a temporary PNG file from an R plot object and displays it.
    It handles the configuration of the image device, plotting, and cleanup.

    Args:
        data: The R object to be plotted.

        image_args: Dictionary containing image configuration parameters:
            - res (int): Resolution in DPI (default: 300)

            - width (float): Width in inches (default: 10)

            - height (float): Height in inches (default: 6)

        **kwargs: Additional keyword arguments passed to R's base::plot function.

    Returns:
        str: Absolute path to the saved temporary PNG image file.

    Note:
        The function creates a temporary directory and file that should be cleaned up
        after use. The image is displayed using the ``show_local_image`` function.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "base_plot.jpeg")

    # Process image args
    image_args = image_args if image_args else {}

    # Define image properties
    image_res = image_args.get("res", 300)
    image_width = int(image_args.get("width", 10) * image_res)
    image_height = int(image_args.get("height", 6) * image_res)

    # Enable image device
    r_pkg_grdevices.jpeg(
        file=file_path, width=image_width, height=image_height, res=image_res
    )

    # Save the tmap plot using R
    r_fnc_plot(data, **kwargs)

    r_pkg_grdevices.dev_off()

    # Display the saved image
    show_local_image(file_path)

    return file_path


#
# High-level operation
#
def plot_base(
    instance: Any, image_args: ImageArgs | None = None, **kwargs: Any
) -> None:
    """Generate and display a base R plot.

    This is a high-level function that wraps ``_base_plot`` to create and display
    a plot using R's base plotting system. It handles the creation of a temporary
    PNG file and displays it.

    Args:
        instance: The R object to be plotted.

        image_args: Dictionary containing image configuration parameters:
            - res (int): Resolution in DPI (default: 300)

            - width (float): Width in inches (default: 10)

            - height (float): Height in inches (default: 6)

        **kwargs: Additional keyword arguments passed to R's base::plot function.

    Returns:
        None: Nothing.

    Note:
        The function creates a temporary directory and file that should be cleaned up
        after use. The image is displayed using the ``show_local_image`` function.
    """
    # Save and display the plot
    _base_plot(instance, image_args=image_args, **kwargs)
