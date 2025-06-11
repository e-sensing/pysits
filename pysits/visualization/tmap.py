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

"""Tmap plot module."""

import os
import tempfile

from rpy2.robjects import r as ro
from rpy2.robjects.robject import RObject

from pysits.backend.functions import r_fnc_plot
from pysits.visualization.image import show_local_image


#
# Utility function
#
def _show_tmap_plot(r_tmap_plot: RObject, image_args: dict = None, **kwargs) -> None:
    """Show an R tmap plot.

    Args:
        r_tmap_plot (rpy2.robjects.RObject): The R tmap plot object.

        **kwargs (dict): Additional keyword arguments passed to ``tmap::tmap_save``.

    Returns:
        None: Nothing.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "tmap_plot.jpeg")

    # Process image args
    image_args = image_args if image_args else {}

    # Define image properties
    image_res = image_args.get("res", 300)
    image_width = int(image_args.get("width", 10) * image_res)
    image_height = int(image_args.get("height", 6) * image_res)

    kwargs.setdefault("dpi", image_res)
    kwargs.setdefault("width", image_width)
    kwargs.setdefault("height", image_height)

    # Save the tmap plot using R
    ro("tmap::tmap_save")(r_tmap_plot, filename=file_path, **kwargs)

    # Display the saved image
    show_local_image(file_path)


#
# High-level operation
#
def plot_tmap(instance: RObject, **kwargs) -> None:
    """Generates and saves a tmap plot, then displays it.

    Args:
        instance (rpy2.robjects.RObject): The R object instance for plotting.

        **kwargs (dict): Additional keyword arguments passed to ``tmap::tmap_save``.

    Returns:
        None: Nothing.
    """
    # Generate the R plot
    tmap_plot = r_fnc_plot(instance, **kwargs)

    # Save and display the plot
    _show_tmap_plot(tmap_plot)
