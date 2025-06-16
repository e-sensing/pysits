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

"""Vector conversions."""

from typing import Any

import numpy as np
from pandas import DataFrame as PandasDataFrame
from rpy2.robjects import DataFrame as RDataFrame
from rpy2.robjects.vectors import Matrix, Vector

from pysits.backend.functions import r_fnc_as_data_frame, r_fnc_colnames, r_fnc_rownames
from pysits.backend.pkgs import r_pkg_base
from pysits.conversions.common import convert_to_python


def vector_to_pandas(vector: Vector) -> PandasDataFrame:
    """Convert a vector to a pandas dataframe."""
    # Get column names
    colnames = r_pkg_base.names(vector)
    colnames = convert_to_python(colnames, as_type="str")

    # Get values
    values = convert_to_python(vector, as_type="float")

    return PandasDataFrame({k: [v] for k, v in zip(colnames, values)})


def matrix_to_pandas(matrix: Matrix) -> PandasDataFrame:
    """Convert a named R matrix to a pandas DataFrame.

    This function takes an R matrix and converts it to a pandas DataFrame
    while preserving row and column names. It handles the conversion of R
    data types to Python types by carefully unwrapping R vectors and lists.

    Args:
        matrix: An R matrix object to be converted.

    Returns:
        A pandas DataFrame containing the data from the R matrix, with preserved row
        and column names. The data types are converted to appropriate Python types.

    Note:
        The function attempts to unwrap single-element R vectors/lists to simplify
        the data structure. If unwrapping fails, the original element is preserved.
    """
    # Convert R matrix to R data.frame for easier column access
    r_df: RDataFrame = r_fnc_as_data_frame(matrix)

    # Extract column and row names from the R data.frame
    colnames: list[str] = list(r_fnc_colnames(r_df))
    rownames: list[str] = list(r_fnc_rownames(r_df))

    # Initialize dictionary to store column data
    data: dict[str, list[Any]] = {}

    # Process each column from the R data.frame
    for col in colnames:
        # Extract R column vector using rx2 accessor
        r_col = r_df.rx2(col)

        # Convert R column elements to Python types
        py_col: list[Any] = []
        for elem in r_col:
            try:
                # Unwrap single-element vectors/lists for cleaner data structure
                if hasattr(elem, "__len__") and len(elem) == 1:
                    py_col.append(elem[0])
                else:
                    py_col.append(elem)
            except Exception:
                # Preserve original element if unwrapping fails
                py_col.append(elem)

        data[col] = py_col

    # Create pandas DataFrame with the processed data and row indices
    return PandasDataFrame(data, index=rownames)


def table_to_pandas(table) -> PandasDataFrame:
    """Convert an R table to a pandas DataFrame.

    This function takes an R table (typically used for contingency
    tables and frequency data)and converts it to a pandas DataFrame
    while preserving the structure and names. It handles both
    1-dimensional and 2-dimensional tables.

    Args:
        table: An R table object to be converted.

    Returns:
        A pandas DataFrame containing the data from the R table, with
        preserved dimension names and structure. For 2D tables, rows
        represent the first dimension and columns represent the second
        dimension.
    """
    # Get the table's dimensions
    dims = table.dim
    if len(dims) > 2:  # noqa: PLR2004 Number of dimensions
        raise ValueError("Only 1D and 2D tables are supported")

    # Get the dimension names (these are the categories for each dimension)
    dimnames = table.dimnames

    # Convert table data to numpy array for easier manipulation
    data = np.array(table)

    if len(dims) == 1:
        # For 1D tables, create a single-column DataFrame
        return PandasDataFrame(
            {dimnames[0][0]: data},  # Use first dimension name as column name
            index=list(dimnames[0]),  # Categories as index
        )

    else:
        # For 2D tables, preserve the structure with rows and columns
        return PandasDataFrame(
            data,
            index=list(dimnames[0]),  # First dimension categories as row labels
            columns=list(dimnames[1]),  # Second dimension categories as column labels
        )
