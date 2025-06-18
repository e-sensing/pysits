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

"""Time-series data models."""

from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from pandas import Series as PandasSeries
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.conversions.tibble import tibble_sits_to_pandas
from pysits.conversions.tibble_arrow import (
    pandas_sits_to_tibble_arrow,
    tibble_sits_to_pandas_arrow,
)
from pysits.models.data.frame import SITSFrame, SITSFrameSF


#
# Time-series data class
#
class SITSTimeSeriesItemModel(PandasSeries):
    """SITS time-series item model."""

    #
    # Attributes
    #
    _instance: RDataFrame = None
    """R DataFrame instance."""

    required_columns: list[str] = [
        "start_date",
        "end_date",
        "time_series",
    ]
    """Required columns for a valid time-series item."""

    def __init__(self, data: PandasSeries, **kwargs):
        """Initializer."""
        # Create a cube from a Pandas Series
        if isinstance(data, PandasSeries):
            # Check if required columns are present
            has_required_columns = all(
                col in data.index for col in self.required_columns
            )

            if has_required_columns:
                # Convert to Pandas DataFrame
                ts_data = PandasDataFrame([data])

                # Convert to R DataFrame
                self._instance = pandas_sits_to_tibble_arrow(ts_data)

        # Initialize super class
        super().__init__(data=data, **kwargs)


class SITSTimeSeriesModel(SITSFrame):
    """Time-series base class."""

    def __init__(self, instance, **kwargs):
        """Initializer."""
        # If instance is a Pandas DataFrame, convert to R cube
        if isinstance(instance, PandasDataFrame):
            # Convert to R DataFrame
            self._instance = pandas_sits_to_tibble_arrow(instance)

        else:
            self._instance = instance

        # Proxy instance
        if isinstance(instance, RDataFrame):
            instance = self._convert_from_r(instance)

        # Initialize super class
        PandasDataFrame.__init__(self, data=instance, **kwargs)

    #
    # Properties
    #
    @property
    def _constructor_sliced(self):
        """Return the constructor for sliced data."""
        return SITSTimeSeriesItemModel

    #
    # Convertions
    #
    def _convert_from_r(self, instance: RDataFrame, **kwargs) -> PandasDataFrame:
        """Convert data from R to Python.

        Args:
            instance (rpy2.robjects.vectors.DataFrame): Data instance.
        """
        return tibble_sits_to_pandas_arrow(instance)

    #
    # Data management
    #
    def _sync_instance(self):
        """Sync instance with R."""
        if not self._is_updated:
            return

        # Save current classes
        classes = self._instance.rclass

        # Update instance
        self._instance = pandas_sits_to_tibble_arrow(self)

        # Restore classes
        self._instance.rclass = classes


class SITSTimeSeriesSFModel(SITSFrameSF):
    """SITS time-series model as sf."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super().__init__(*args, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance: RDataFrame, **kwargs) -> GeoPandasDataFrame:
        """Convert data from R to Python.

        Args:
            instance (rpy2.robjects.vectors.DataFrame): Data instance.
        """
        return tibble_sits_to_pandas(instance)


class SITSTimeSeriesPatternsModel(SITSTimeSeriesModel):
    """SITS patterns model."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super().__init__(*args, **kwargs)


class SITSTimeSeriesClassificationModel(SITSTimeSeriesModel):
    """SITS time-series classification model."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        super().__init__(*args, **kwargs)
