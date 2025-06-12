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

import numpy as np
from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from rpy2.rinterface_lib.sexp import NULLType
from rpy2.robjects.vectors import DataFrame as RDataFrame
from rpy2.robjects.vectors import FloatMatrix, IntVector

from pysits.backend.functions import r_fnc_class
from pysits.conversions.base import convert_to_python
from pysits.conversions.matrix import matrix_to_pandas, table_to_pandas
from pysits.conversions.tibble import tibble_nested_to_pandas, tibble_to_pandas
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
    def _convert_from_r(self, instance, **kwargs):
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


class SITSFrameBase(SITSData):
    """Base class for SITS Data."""

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
    # Operations
    #
    def take(self, indices, axis=0, *args, **kwargs):
        """Take elements from the R data.frame along the specified axis."""
        indices = np.atleast_1d(indices)
        r_indices = IntVector((indices + 1).tolist())

        # ToDo: review transformations to R
        if isinstance(self._instance, PandasDataFrame):
            return self._instance.take(indices, axis, **kwargs)

        if axis == 0:
            # Take rows: [r_indices, ]
            result = self._instance.rx(r_indices, True)

        elif axis == 1:
            # Take columns: [, r_indices]
            result = self._instance.rx(True, r_indices)

        else:
            raise ValueError("Axis must be 0 (rows) or 1 (columns)")

        return self._constructor(result)

    #
    # Convertions
    #
    def _convert_from_r(self, instance, **kwargs):
        """Convert data from R to Python."""
        return tibble_to_pandas(instance)


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
        PandasDataFrame.__init__(self, data=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance, **kwargs):
        """Convert data from R to Python."""
        return vector_to_pandas(instance)


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


class SITSTable(SITSFrame):
    """Base class for sits table results."""

    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        self._instance = instance

        # Proxy instance
        if "table" in r_fnc_class(instance):
            instance = self._convert_from_r(instance)

        # Initialize super class
        PandasDataFrame.__init__(self, data=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance, **kwargs):
        """Convert data from R to Python."""
        return table_to_pandas(instance)


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


class SITSAccuracy(SITSData):
    """Base class for sits accuracy results."""

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
    def error_matrix(self) -> SITSConfusionMatrix:
        """Error matrix property."""
        return SITSTable(self._instance.rx2("error_matrix"))

    @property
    def area_pixels(self) -> SITSTable:
        """Area pixels property."""
        return SITSNamedVector(self._instance.rx2("area_pixels"))

    @property
    def error_ajusted_area(self) -> SITSNamedVector:
        """Error adjusted area property."""
        return SITSNamedVector(self._instance.rx2("error_ajusted_area"))

    @property
    def stderr_prop(self) -> SITSNamedVector | SITSMatrix:
        """Standard error property."""
        return SITSNamedVector(self._instance.rx2("stderr_prop"))

    @property
    def stderr_area(self) -> SITSNamedVector | SITSMatrix:
        """Standard error area property."""
        return SITSNamedVector(self._instance.rx2("stderr_area"))

    @property
    def conf_interval(self) -> SITSNamedVector | SITSMatrix:
        """Confidence interval property."""
        return SITSNamedVector(self._instance.rx2("conf_interval"))

    @property
    def accuracy(self) -> SITSNamedVector:
        """Accuracy property."""
        value = convert_to_python(self._instance.rx2("accuracy"), as_type=None)
        value = {k: v for d in value for k, v in d.items()}

        # Updating user and producer values
        value["user"] = PandasDataFrame(value["user"], index=[0])
        value["producer"] = PandasDataFrame(value["producer"], index=[0])

        # Return
        return value

    #
    # Dunder methods
    #
    def __str__(self):
        """String representation."""
        return str(self._instance)

    def __repr__(self):
        """Representation."""
        return str(self._instance)
