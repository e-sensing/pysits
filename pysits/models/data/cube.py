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

"""Cube models."""

from pandas import DataFrame as PandasDataFrame
from pandas import Series as PandasSeries
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.backend.functions import r_fnc_set_column
from pysits.conversions.tibble_arrow import (
    pandas_cube_to_tibble_arrow,
    tibble_cube_to_pandas_arrow,
)
from pysits.models.data.frame import SITSFrame


#
# Base class
#
class SITSCubeItemModel(PandasSeries):
    """SITS Data Cube item model.

    Attributes:
        _instance (RDataFrame): R DataFrame instance containing the cube data.

        required_columns (list[str]): List of required column names for a valid
            cube item.
    """

    #
    # Attributes
    #
    _instance: RDataFrame = None
    """R DataFrame instance."""

    required_columns: list[str] = [
        "source",
        "collection",
        "satellite",
        "sensor",
        "tile",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "crs",
        "file_info",
    ]
    """Required columns for a valid cube item."""

    def __init__(self, data: PandasSeries, **kwargs) -> None:
        """Initialize a SITS Data Cube item.

        Args:
            data (PandasSeries): Input data containing cube metadata and information.

            **kwargs: Additional keyword arguments passed to pandas.Series constructor.

        Note:
            The input data must contain all required columns specified in
            ``required_columns``. If the data is valid, it will be converted
            to an R DataFrame instance.
        """
        # Create a cube from a Pandas Series
        if isinstance(data, PandasSeries) and getattr(data, "_instance", None) is None:
            # Check if required columns are present
            has_required_columns = all(
                col in data.index for col in self.required_columns
            )

            if has_required_columns:
                # Convert to Pandas DataFrame
                cube_data = PandasDataFrame([data])

                # Convert to R DataFrame
                self._instance = pandas_cube_to_tibble_arrow(cube_data)

        # Initialize super class
        super().__init__(data=data, **kwargs)


class SITSCubeModel(SITSFrame):
    """SITS Data Cube data.

    Attributes:
        _instance (RDataFrame): R DataFrame instance containing the cube data.
    """

    #
    # Attributes
    #
    required_columns: list[str] = [
        "source",
        "collection",
        "satellite",
        "sensor",
        "tile",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "crs",
        "file_info",
    ]
    """Required columns for a valid cube."""

    #
    # Properties
    #
    @property
    def _constructor_sliced(self):
        """Return the constructor for sliced data."""
        return SITSCubeItemModel

    #
    # Dunder methods
    #
    def __init__(self, instance, **kwargs):
        """Initializer."""
        # If instance is a Pandas DataFrame, convert to R cube
        if isinstance(instance, PandasDataFrame):
            # Check if required columns are present
            has_required_columns = all(
                col in instance.columns for col in self.required_columns
            )

            if has_required_columns:
                self._instance = pandas_cube_to_tibble_arrow(instance)

        else:
            self._instance = instance

        # Proxy instance
        if isinstance(instance, RDataFrame):
            instance = self._convert_from_r(instance)

        # Initialize super class
        PandasDataFrame.__init__(self, data=instance, **kwargs)

    #
    # Convertions
    #
    def _convert_from_r(self, instance: RDataFrame) -> PandasDataFrame:
        """Convert data from R to Python.

        Args:
            instance (rpy2.robjects.vectors.DataFrame): Data instance.
        """
        return tibble_cube_to_pandas_arrow(instance)

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
        base_info = None

        if "base_info" in self.columns:
            # Convert each dataframe in the series to R DataFrame
            base_info = [pandas_cube_to_tibble_arrow(df) for df in self.base_info]

            # Drop base_info
            self.drop(columns=["base_info"], inplace=True)

        self._instance = pandas_cube_to_tibble_arrow(self)

        # Add base_info
        if base_info is not None:
            self._instance = r_fnc_set_column(self._instance, "base_info", base_info)

        # Restore classes
        self._instance.rclass = classes

    #
    # Representation
    #
    def _repr_html_(self) -> str:
        """Create an HTML representation of the cube."""
        from pysits.jinja import get_template

        # Get the HTML for the cube table from pandas
        super_html = super()._repr_html_() if hasattr(super(), "_repr_html_") else ""

        # Render the template
        return get_template("cube.html").render(
            cube_obj=self,
            super_html=super_html,
        )
