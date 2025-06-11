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

"""Leaflet utilities."""

import os
import webbrowser

from rpy2.robjects.robject import RObject
from rpy2.robjects.vectors import ListVector

from pysits.backend.pkgs import r_pkg_htmlwidgets, r_pkg_sits

# Optional: only import IPython if available
try:
    from IPython.display import IFrame, display

    _IPYTHON_AVAILABLE = True

except ImportError:
    _IPYTHON_AVAILABLE = False


def _show_leaflet_widget(
    r_leaflet_widget: ListVector, width: str = "100%", height: str = "600px"
) -> None:
    """Save and display an R htmlwidget (leaflet map).

    Args:
        r_leaflet_widget: R object of class ``leaflet``/``htmlwidget`` (e.g. from
                          ``sits_view``).

        width: Width for display in Jupyter notebook (default: ``'100%'``).

        height: Height for display in Jupyter notebook (default: ``'600px'``)

    Returns:
        None: Nothing.
    """
    # Save to temporary HTML file
    tmp_path = "sits-map.html"

    # Save using R's saveWidget
    r_pkg_htmlwidgets.saveWidget(r_leaflet_widget, tmp_path, selfcontained=True)

    # Detect if we're in Jupyter (simple heuristic)
    in_jupyter = False
    try:
        from IPython import get_ipython

        if "IPKernelApp" in get_ipython().config:
            in_jupyter = True

    except Exception:  # noqa: E722
        pass

    # Display accordingly
    if in_jupyter and _IPYTHON_AVAILABLE:
        display(IFrame(src=tmp_path, width=width, height=height))

    else:  # noqa: E722
        webbrowser.open("file://" + os.path.realpath(tmp_path))

    # Remove the temporary file
    # os.unlink(tmp_path)


def plot_leaflet(instance: RObject, **kwargs) -> None:
    """Plot a leaflet map.

    Args:
        instance: The instance to plot.

        **kwargs: Additional keyword arguments passed to ``sits_view``.
    """
    # Generate the R plot
    leaflet_plot = r_pkg_sits.sits_view(instance, **kwargs)

    # Display the plot
    _show_leaflet_widget(leaflet_plot)
