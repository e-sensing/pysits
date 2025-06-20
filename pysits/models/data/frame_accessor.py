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
# MERCHANTABILITY or FITNESS FOR ANY PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#

"""Frame data accessor for SITS (Satellite Image Time Series) data management.

This module provides a custom pandas DataFrame accessor that enables seamless
interaction with SITS data frames. The accessor provides methods to manage
sample properties such as labels, ensuring proper integration between Python
pandas DataFrames and the underlying R SITS package.

The SITSAccessor class extends pandas DataFrames with SITS-specific functionality,
allowing users to work with satellite image time series data in a familiar
pandas interface while maintaining compatibility with the R SITS ecosystem.
"""

import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from rpy2.robjects.vectors import StrVector

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.common import convert_to_python


@register_dataframe_accessor("sits")
class SITSAccessor:
    """Custom pandas DataFrame accessor for SITS (Satellite Image Time Series) data.

    This accessor provides SITS-specific functionality to pandas DataFrames,
    enabling management of data properties such as sample labels.

    The accessor is automatically registered with pandas and can be accessed
    via the `.sits` attribute on any DataFrame that contains SITS data.

    Attributes:
        _obj (pd.DataFrame): The pandas DataFrame object that this accessor
            is attached to.

    Example:
        >>> import pysits
        >>> # Assuming df is a DataFrame with SITS data
        >>> df.sits.labels  # Get current labels
        >>> df.sits.labels = ["forest", "deforestation"]  # Set new labels
    """

    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        """Initialize the SITS accessor with a pandas DataFrame.

        Args:
            pandas_obj: The pandas DataFrame to attach this accessor to.
        """
        self._obj = pandas_obj

    def _check_instance(self) -> bool:
        """Check if the DataFrame contains valid SITS data.

        This method verifies that the DataFrame has an `_instance` attribute
        that points to a valid R SITS object. This is a prerequisite for
        all SITS-specific operations.

        Returns:
            True if the DataFrame contains valid SITS data.

        Raises:
            ValueError: If the DataFrame does not contain valid SITS data
                (i.e., missing `_instance` attribute).
        """
        if getattr(self._obj, "_instance", None):
            return True

        raise ValueError("Data is not a SITS data frame.")

    @property
    def labels(self) -> list[str]:
        """Get the sample labels from the SITS data frame.

        This property retrieves the current sample labels from the underlying
        R SITS object and converts them to a Python list of strings.

        Returns:
            A list of strings representing the current sample labels in the
            SITS data frame.

        Raises:
            ValueError: If the DataFrame does not contain valid SITS data.

        Example:
            >>> df.sits.labels
            ['forest', 'deforestation', 'water']
        """
        self._check_instance()
        return convert_to_python(r_pkg_sits.sits_labels(self._obj._instance))

    @labels.setter
    def labels(self, new_labels: list[str] | tuple) -> None:
        """Set new sample labels for the SITS data frame.

        This setter updates the sample labels in the underlying R SITS object.

        Args:
            new_labels: A list or tuple of strings representing the new
                sample labels to assign to the SITS data frame.

        Raises:
            ValueError: If the DataFrame does not contain valid SITS data.

        Example:
            >>> df.sits.labels = ["forest", "deforestation", "water"]
            >>> df.sits.labels  # ['forest', 'deforestation', 'water']
        """
        self._check_instance()

        # Get label setter function from R SITS package
        r_set_labels_func = getattr(r_pkg_sits, "sits_labels<-")

        # Convert labels to R vector
        r_labels = StrVector(new_labels)

        # Set labels in the R SITS object
        self._obj._instance = r_set_labels_func(self._obj._instance, r_labels)
