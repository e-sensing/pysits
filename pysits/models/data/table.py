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

"""Table data models."""

from pandas import DataFrame as PandasDataFrame

from pysits.backend.functions import r_fnc_class
from pysits.conversions.vector import table_to_pandas
from pysits.models.data.frame import SITSFrame


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
