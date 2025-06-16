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

"""Accuracy data models."""

from pandas import DataFrame as PandasDataFrame

from pysits.conversions.common import convert_to_python
from pysits.models.data.base import SITSData
from pysits.models.data.matrix import SITSConfusionMatrix, SITSMatrix
from pysits.models.data.table import SITSTable
from pysits.models.data.vector import SITSNamedVector


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
