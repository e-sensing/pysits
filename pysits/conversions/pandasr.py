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

"""Pandas to R conversion utilities."""

import warnings

from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.backend.pkgs import r_pkg_sf


def pandas_to_r(data: PandasDataFrame) -> RDataFrame:
    """Convert a pandas DataFrame to an R DataFrame object.

    This function converts a pandas DataFrame to an R DataFrame using
    rpy2's conversion infrastructure. It handles the conversion context
    to ensure proper type mapping between Python and R objects.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.

    Returns:
        rpy2.robjects.vectors.DataFrame: The converted R DataFrame object.

    Notes:
        - The function uses rpy2's localconverter to ensure proper conversion context
        - Handles both DataFrame and non-DataFrame inputs
        - Preserves column names and data types where possible
        - For non-DataFrame inputs, falls back to rpy2's default converter
    """
    with localconverter(robjects.default_converter + pandas2ri.converter):
        return robjects.conversion.py2rpy(data)


def geopandas_to_r(data: GeoPandasDataFrame) -> RDataFrame:
    """Convert pandas DataFrame or GeoDataFrame to R DataFrame or sf object.

    Removes columns that contain embedded pandas DataFrames.
    """
    data = GeoPandasDataFrame(data)

    if data.crs is None:
        raise ValueError("GeoDataFrame must have a CRS")

    # Identify columns where no cell is a DataFrame
    safe_columns = [col for col in data.columns if not data[col].dtype.name == "sits"]

    # Warn if columns are dropped
    dropped_columns = set(data.columns) - set(safe_columns)
    if dropped_columns:
        warnings.warn(
            f"Warning: Dropping columns with embedded DataFrames: {dropped_columns}"
        )

    # Keep only safe columns
    data_safe = data[safe_columns].copy()

    # If GeoDataFrame, convert geometry to WKT and include geometry column
    if isinstance(data, GeoPandasDataFrame):
        geom_col = data.geometry.name
        data_safe[geom_col] = data.geometry.to_wkt()

    # Convert to R DataFrame
    with localconverter(robjects.default_converter + pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(data_safe)

    # If GeoDataFrame, convert to sf
    if isinstance(data, GeoPandasDataFrame):
        r_df = r_pkg_sf.st_as_sf(
            r_df,
            wkt=robjects.StrVector([geom_col]),
            crs=robjects.StrVector([data.crs.to_wkt()]),
        )

    return r_df
