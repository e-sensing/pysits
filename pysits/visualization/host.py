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

"""Handover of figures to the host environment."""

import matplotlib.pyplot as plt

from pysits.models.visual import SITSPlot, SITSPlotList, display_hook_installed


#
# High-level operations
#
def display_figures(plot: SITSPlot | SITSPlotList) -> None:
    """Display figures.

    This functions displays the figures of a plot such that hosts
    can collect them. This is required as hosts such as `knitr` intercept
    `pyplot.show` to collect what is being shown. Images are shown one at a time,
    so we give the opportunity to host collect and manage each figure separately.

    Does nothing when no host is listening.

    Args:
        plot (SITSPlot | SITSPlotList): The plot to display.

    Returns:
        None: Nothing.
    """
    if not display_hook_installed():
        return

    plots = [plot] if isinstance(plot, SITSPlot) else list(plot)

    for single in plots:
        # Create the canvas
        options = single.options
        canvas = plt.figure(
            figsize=(options.width, options.height),
            dpi=options.dpi,
        )

        # Draw the figure on the canvas
        single.to_matplotlib(canvas)

        # Show!
        plt.show()

        # Close the canvas
        plt.close(canvas)
