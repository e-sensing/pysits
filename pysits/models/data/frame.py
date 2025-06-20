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

"""Frame data models."""

from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.conversions.tibble import (
    pandas_to_tibble,
    tibble_nested_to_pandas,
    tibble_to_pandas,
)
from pysits.models.data.base import SITSData


class SITSFrameBase(SITSData):
    """Base class for SITS Data."""

    _is_updated = False
    """Whether the instance is updated."""

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate metadata from another object to the current one.

        This method is called by pandas during internal operations that return a new
        object derived from an existing one, such as slicing, copying, arithmetic,
        joins, merges, and others. It ensures that any custom metadata defined in the
        ``_metadata`` attribute is preserved in the result.
        """
        if isinstance(other, SITSData):
            for name in self._metadata:
                setattr(self, name, getattr(other, name, None))
        return self

    #
    # Properties (Internal)
    #
    @property
    def _constructor(self):
        # Always return the current subclass
        return self.__class__

    def __setitem__(self, key, value):
        """Set item."""
        super().__setitem__(key, value)
        self._is_updated = True

    #
    # Convertions
    #
    def _convert_from_r(self, instance, **kwargs):
        """Convert data from R to Python."""
        return tibble_to_pandas(instance)

    #
    # Data management
    def _sync_instance(self):
        """Sync instance with R."""
        if not self._is_updated:
            return

        self._instance = pandas_to_tibble(self)

        # Update flag
        self._is_updated = False


class SITSFrame(SITSFrameBase, PandasDataFrame):
    """Base class for sits frame results."""

    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        self._instance = instance

        # Proxy instance
        if isinstance(instance, RDataFrame):
            instance = self._convert_from_r(instance)

        # Initialize super class
        PandasDataFrame.__init__(self, data=instance, **kwargs)


class SITSFrameSF(SITSFrameBase, GeoPandasDataFrame):
    """Base class for sits frame as sf."""

    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        self._instance = instance

        # Proxy instance
        if isinstance(instance, RDataFrame):
            instance = self._convert_from_r(instance)

        # Initialize super class
        GeoPandasDataFrame.__init__(self, data=instance, **kwargs)


class SITSFrameNested(SITSFrame):
    """General class for sits frame with embedded data frames."""

    # Dunder methods
    #
    def __init__(self, instance, nested_columns, **kwargs):
        """Initializer."""
        self._instance = instance

        # Proxy instance
        if isinstance(instance, RDataFrame):
            instance = self._convert_from_r(instance, nested_columns)

        # Initialize super class
        PandasDataFrame.__init__(self, data=instance, **kwargs)

    def _convert_from_r(self, instance, nested_columns, **kwargs):
        """Convert data from R to Python."""
        return tibble_nested_to_pandas(instance, nested_columns=nested_columns)
