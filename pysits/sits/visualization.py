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

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import rpy2_fix_type
from pysits.models.data.base import SITStructureData
from pysits.models.data.cube import SITSCubeItemModel, SITSCubeModel
from pysits.models.data.frame import SITSFrame
from pysits.models.data.ts import (
    SITSTimeSeriesClassificationModel,
    SITSTimeSeriesModel,
    SITSTimeSeriesPatternsModel,
)
from pysits.models.ml import SITSMachineLearningMethod
from pysits.visualization import plot_base, plot_leaflet, plot_tmap


#
# Interactive plot
#
@rpy2_fix_type
def sits_view(data: object, **kwargs) -> None:
    """sits view as dispatch."""
    return plot_leaflet(data, **kwargs)


#
# Static plot (dispatch chain)
#
@singledispatch
@rpy2_fix_type
def sits_plot(data: object, **kwargs) -> None:
    """sits plot as dispatch."""
    # Assuming data is a "raw rpy2" object
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSFrame, **kwargs) -> None:
    """Plot Frame data."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITStructureData, **kwargs) -> None:
    """Plot Structure data."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSCubeModel, **kwargs) -> None:
    """Plot cube."""
    return plot_tmap(data, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSCubeItemModel, **kwargs) -> None:
    """Plot cube."""
    return plot_tmap(data, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSTimeSeriesModel, **kwargs) -> None:
    """Plot time-series."""
    # Check if the time-series has multiple bands or labels
    is_multiple_1 = len(r_pkg_sits.sits_bands(data)) > 1
    is_multiple_2 = len(r_pkg_sits.sits_labels(data)) > 1

    # Define if is multiple
    is_multiple = data.nrow > 1 and (is_multiple_1 or is_multiple_2)

    # Special case: SOM clean samples
    if "som_clean_samples" in data.rclass:
        is_multiple = False

    # Plot the time-series
    return plot_base(data, multiple=is_multiple, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSTimeSeriesClassificationModel, **kwargs) -> None:
    """Plot time-series classification."""
    is_multiple = data.nrow > 1
    return plot_base(data, multiple=is_multiple, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSTimeSeriesPatternsModel, **kwargs) -> None:
    """Plot patterns."""
    return plot_base(data, multiple=False, **kwargs)


@sits_plot.register
@rpy2_fix_type
def _(data: SITSMachineLearningMethod, **kwargs) -> None:
    """Plot machine learning method."""
    return plot_base(data, **kwargs)
