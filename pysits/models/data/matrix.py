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

"""Matrix data models."""

from pandas import DataFrame as PandasDataFrame
from rpy2.rinterface_lib.sexp import NULLType
from rpy2.robjects.vectors import FloatMatrix

from pysits.backend.functions import r_fnc_class
from pysits.conversions.common import convert_to_python
from pysits.conversions.vector import matrix_to_pandas
from pysits.models.data.base import SITSData
from pysits.models.data.frame import SITSFrame
from pysits.models.data.table import SITSTable
from pysits.models.data.vector import SITSNamedVector


class SITSMatrix(SITSFrame):
    """Base class for sits matrix results."""

    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        self._instance = instance

        # Proxy instance
        if "matrix" in r_fnc_class(instance):
            instance = self._convert_from_r(instance)

        # Initialize super class
        PandasDataFrame.__init__(self, data=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance, **kwargs):
        """Convert data from R to Python."""
        return matrix_to_pandas(instance)


class SITSConfusionMatrix(SITSData):
    """Base class for sits confusion matrix results."""

    #
    # Convertions
    #
    def _convert_from_r(self, instance):
        """Convert data from R to Python."""
        return instance

    #
    # Properties
    #
    @property
    def positive(self) -> str | None:
        """Positive property."""
        value = self._instance.rx2("positive")
        is_null = isinstance(value, NULLType)

        return str(value[0]) if not is_null else None

    @property
    def table(self) -> SITSTable:
        """Table property."""
        return SITSTable(self._instance.rx2("table"))

    @property
    def overall(self) -> SITSNamedVector:
        """Overall property."""
        return SITSNamedVector(self._instance.rx2("overall"))

    @property
    def by_class(self) -> SITSNamedVector | SITSMatrix:
        """By class property."""
        value = self._instance.rx2("byClass")
        is_matrix = isinstance(value, FloatMatrix)

        return SITSNamedVector(value) if not is_matrix else SITSMatrix(value)

    @property
    def mode(self) -> str | None:
        """Mode property."""
        value = self._instance.rx2("mode")
        is_null = isinstance(value, NULLType)

        return str(value[0]) if not is_null else None

    @property
    def dots(self) -> list:
        """Dots property."""
        return convert_to_python(self._instance.rx2("dots"))

    #
    # Dunder methods
    #
    def __str__(self):
        """String representation."""
        return str(self._instance)

    def __repr__(self):
        """Representation."""
        return str(self._instance)
