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

"""time-series models."""

from pandas import DataFrame as PandasDataFrame
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.models.base import SITSData
from pysits.toolbox.conversions.tibble import tibble_sits_to_pandas, tibble_to_pandas


#
# Time-series data class
#
class SITSTimeSeriesModel(SITSData):
    """Time-series base class."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super().__init__(*args, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance: RDataFrame) -> PandasDataFrame:
        """Convert data from R to Python.

        Args:
            instance (rpy2.robjects.vectors.DataFrame): Data instance.
        """
        return tibble_sits_to_pandas(instance)


#
# Predictors
#
class SITSPredictors(SITSData):
    """Time-series predictors."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super().__init__(*args, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance: RDataFrame) -> PandasDataFrame:
        """Convert data from R to Python.

        Args:
            instance (rpy2.robjects.vectors.DataFrame): Data instance.
        """
        return tibble_to_pandas(instance)


#
# Self-organized maps
#
class SITSOMData(SITSData):
    """Self-organized maps (SOM) data."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super().__init__(*args, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert object from R to Python."""
        return instance
