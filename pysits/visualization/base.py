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
import shutil
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
def _base_plot(
    data: Any,
    image_args: ImageArgs | None = None,
    multiple: bool = False,
    **kwargs: Any,
) -> None:
    """Save and show images created using base plot.

    This function creates temporary PNG files from R plot objects and displays them.
    It handles the configuration of the image device, plotting, and cleanup.
    The function handles multiple plots returned by r_fnc_plot as a ListVector.

    Args:
        data: The R object to be plotted.

        image_args: Dictionary containing image configuration parameters:
            - res (int): Resolution in DPI (default: 300)

            - width (float): Width in inches (default: 10)

            - height (float): Height in inches (default: 6)

        multiple: Whether to plot multiple plots.

        **kwargs: Additional keyword arguments passed to R's base::plot function.

    Returns:
        None: Nothing.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Process image args
    image_args = image_args if image_args else {}

    # Define image properties
    image_res = image_args.get("res", 300)
    image_width = int(image_args.get("width", 10) * image_res)
    image_height = int(image_args.get("height", 6) * image_res)

    # Plot data
    plots = r_fnc_plot(data, **kwargs)

    # Handle plots
    if multiple:
        for i, plot in enumerate(plots):
            for index, figure in enumerate(plot):
                file_path = os.path.join(temp_dir, f"base_plot_{i}_{index}.jpeg")

                # Enable image device
                r_pkg_grdevices.jpeg(
                    file=file_path,
                    width=image_width,
                    height=image_height,
                    res=image_res,
                )

                # Plot the plot object directly
                r_fnc_plot(figure)

                r_pkg_grdevices.dev_off()

                # Display saved image
                show_local_image(file_path)

    else:
        # Assuming a plot is a list of elements, we always have many elements.
        # Cases where we have a single element indicates that the plot object is
        # inside a list.
        while len(plots) == 1:
            plots = plots[0]

        # Create a temporary file
        file_path = os.path.join(temp_dir, "base_plot.jpeg")

        # Enable image device
        r_pkg_grdevices.jpeg(
            file=file_path, width=image_width, height=image_height, res=image_res
        )

        # Save plot using R
        r_fnc_plot(plots)

        r_pkg_grdevices.dev_off()

        # Display saved image
        show_local_image(file_path)

    # Clean up temporary directory
    shutil.rmtree(temp_dir)


#
# High-level operation
#
def plot_base(
    instance: Any,
    image_args: ImageArgs | None = None,
    multiple: bool = False,
    **kwargs: Any,
) -> None:
    """Generate and display base R plots.

    This is a high-level function that wraps ``_base_plot`` to create and display
    a plot using R's base plotting system. It handles the creation of a temporary
    PNG file and displays it.

    Args:
        instance: The R object to be plotted.

        image_args: Dictionary containing image configuration parameters:
            - res (int): Resolution in DPI (default: 300)

            - width (float): Width in inches (default: 10)

            - height (float): Height in inches (default: 6)

        multiple: Whether to plot multiple plots.

        **kwargs: Additional keyword arguments passed to R's base::plot function.

    Returns:
        None: Nothing.
    """
    # Save and display plot
    _base_plot(instance, image_args=image_args, multiple=multiple, **kwargs)
