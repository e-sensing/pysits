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
from pysits.conversions.decorators import rpy2_fix_type, rpy2_fix_type_except
from pysits.docs import attach_doc
from pysits.models.data.base import SITStructureData
from pysits.models.data.cube import SITSCubeItemModel, SITSCubeModel
from pysits.models.data.frame import SITSFrame
from pysits.models.data.ts import (
    SITSTimeSeriesClassificationModel,
    SITSTimeSeriesModel,
    SITSTimeSeriesPatternsModel,
)
from pysits.models.ml import SITSMachineLearningMethod, SITSRepresentationLearningMethod
from pysits.models.visual import ImageArgs, SITSPlot, SITSPlotList
from pysits.visualization import plot_base, plot_leaflet

#
# Type aliases
#
SITSPlotResult = SITSPlot | SITSPlotList


#
# Interactive plot
#
@rpy2_fix_type
@attach_doc("sits_view")
def sits_view(data: object, **kwargs) -> None:
    """sits view as dispatch."""
    return plot_leaflet(data, **kwargs)


#
# Static plot (dispatch chain)
#
@singledispatch
@rpy2_fix_type_except("image_args")
@attach_doc("plot")
def sits_plot(data: object, **kwargs) -> SITSPlotResult:
    """sits plot as dispatch."""
    # Assuming data is a "raw rpy2" object
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSFrame, **kwargs) -> SITSPlotResult:
    """Plot Frame data."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITStructureData, **kwargs) -> SITSPlotResult:
    """Plot Structure data."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSCubeModel, **kwargs) -> SITSPlotResult:
    """Plot cube."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSCubeItemModel, **kwargs) -> SITSPlotResult:
    """Plot cube."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSTimeSeriesModel, **kwargs) -> SITSPlotResult:
    """Plot time-series."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSTimeSeriesClassificationModel, **kwargs) -> SITSPlotResult:
    """Plot time-series classification."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSTimeSeriesPatternsModel, **kwargs) -> SITSPlotResult:
    """Plot patterns."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSMachineLearningMethod, **kwargs) -> SITSPlotResult:
    """Plot machine learning method."""
    return plot_base(data, **kwargs)


@sits_plot.register
@rpy2_fix_type_except("image_args")
def _(data: SITSRepresentationLearningMethod, **kwargs) -> SITSPlotResult:
    """Plot representation learning method."""
    return plot_base(data, **kwargs)


#
# Sankey plot
#
@rpy2_fix_type_except("image_args")
@attach_doc("sits_sankey")
def sits_sankey(*args, image_args: ImageArgs | None = None, **kwargs) -> SITSPlotResult:
    """Plot class trajectories from multi-temporal classified cubes."""
    return plot_base(
        instance=r_pkg_sits.sits_sankey(*args, **kwargs),
        image_args=image_args,
    )
