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

"""base models."""

from pandas import DataFrame
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.conversions.tibble import tibble_to_pandas
from pysits.conversions.vector import vector_to_pandas
from pysits.models.base import SITSBase


class SITSData(SITSBase):
    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        # Convert data
        instance = self._convert_from_r(instance)

        # Initialize super class
        super().__init__(instance=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert data from R to Python."""
        return None


class SITStructureData(SITSData):
    """Base class for sits structure (e.g., list) results."""

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert data from R to Python."""
        return instance


class SITSFrame(DataFrame, SITSData):
    """Base class for SITS Data."""

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
        super().__init__(data=instance, **kwargs)

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

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert data from R to Python."""
        return tibble_to_pandas(instance)


class SITSNamedVector(SITSFrame):
    """Base class for sits named vector results."""

    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        self._instance = instance

        # Convert vector to pandas dataframe
        instance = self._convert_from_r(instance)

        # Initialize super class
        DataFrame.__init__(self, data=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert data from R to Python."""
        return vector_to_pandas(instance)
