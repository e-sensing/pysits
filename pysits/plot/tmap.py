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

from rpy2.robjects import r as ro

from pysits.backend.utils import r_plot
from pysits.plot.toolbox import show_local_image


#
# Utility function
#
def _save_tmap_plot(r_tmap_plot, **kwargs):
    """Saves an R tmap plot to a temporary directory and displays it.

    Args:
        r_tmap_plot (rpy2.robjects.RObject): The R tmap plot object.

        **kwargs (dict): Additional keyword arguments passed to ``tmap::tmap_save``.

    Returns:
        str: Path to the saved image.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "tmap_plot.png")

    # Save the tmap plot using R
    ro("tmap::tmap_save")(r_tmap_plot, filename=file_path, **kwargs)

    # Display the saved image
    return show_local_image(file_path)


#
# High-level operation
#
def plot_tmap(instance, **kwargs):
    """Generates and saves a tmap plot, then displays it.

    Args:
        instance (rpy2.robjects.RObject): The R object instance for plotting.

        **kwargs (dict): Additional keyword arguments passed to ``tmap::tmap_save``.

    Returns:
        str: Path to the saved image.
    """
    # Generate the R plot
    tmap_plot = r_plot(instance, **kwargs)

    # Save and display the plot
    return _save_tmap_plot(tmap_plot)
