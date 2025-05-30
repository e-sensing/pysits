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

from pandas import DataFrame as PandasDataFrame
from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import DataFrame as RDataFrame


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
