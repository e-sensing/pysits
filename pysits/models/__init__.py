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

"""pysits models."""

from .base import SITSBase
from .cube import SITSCubeModel
from .data import (
    SITSData,
    SITSFrame,
    SITSFrameBase,
    SITSFrameNested,
    SITSFrameSF,
    SITSMatrix,
    SITSNamedVector,
    SITSTable,
    SITStructureData,
)
from .ml import SITSMachineLearningMethod
from .ts import (
    SITSTimeSeriesClassificationModel,
    SITSTimeSeriesModel,
    SITSTimeSeriesPatternsModel,
    SITSTimeSeriesSFModel,
)

__all__ = (
    # Base
    "SITSBase",
    "SITSData",
    "SITSFrameBase",
    "SITSFrame",
    "SITSFrameSF",
    "SITSFrameNested",
    "SITStructureData",
    "SITSNamedVector",
    "SITSMatrix",
    "SITSTable",
    # Data Cube
    "SITSCubeModel",
    # Time-series
    "SITSTimeSeriesModel",
    "SITSTimeSeriesSFModel",
    "SITSTimeSeriesPatternsModel",
    "SITSTimeSeriesClassificationModel",
    # Machine-learning
    "SITSMachineLearningMethod",
)
