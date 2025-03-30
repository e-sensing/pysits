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

"""visualization functions."""

from functools import singledispatch

from pysits.backend.utils import r_plot
from pysits.models import SITSCubeModel, SITSTimeSeriesModel
from pysits.toolbox.visualization import plot_tmap


@singledispatch
def sits_plot(data: object):
    """sits plot as dispatch."""


@sits_plot.register
def _(data: SITSCubeModel, **kwargs):
    """Plot cube."""
    return plot_tmap(data._instance, **kwargs)


@sits_plot.register
def _(data: SITSTimeSeriesModel, **kwargs):
    """Plot time-series."""
    return r_plot(data._instance, **kwargs)
