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

"""Visualization functions."""

from functools import singledispatch

from pysits.models import (
    SITSCubeModel,
    SITSFrame,
    SITSTimeSeriesModel,
    SITStructureData,
)
from pysits.visualization import plot_base, plot_tmap


#
# Dispatch chain for plot
#
@singledispatch
def sits_plot(data: object, **kwargs) -> None:
    """sits plot as dispatch."""
    # Assuming data is a "raw rpy2" object
    return plot_base(data, **kwargs)


@sits_plot.register
def _(data: SITSFrame, **kwargs) -> None:
    """Plot Frame data."""
    return plot_base(data._instance, **kwargs)


@sits_plot.register
def _(data: SITStructureData, **kwargs) -> None:
    """Plot Structure data."""
    return plot_base(data._instance, **kwargs)


@sits_plot.register
def _(data: SITSCubeModel, **kwargs) -> None:
    """Plot cube."""
    return plot_tmap(data._instance, **kwargs)


@sits_plot.register
def _(data: SITSTimeSeriesModel, **kwargs) -> None:
    """Plot time-series."""
    return plot_base(data._instance, **kwargs)
