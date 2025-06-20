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

"""Arrow conversions."""

import os
import tempfile
from collections.abc import Callable

from pandas import DataFrame as PandasDataFrame
from pandas.core.generic import NDFrame as PandasNDFrame
from pyarrow import feather
from rpy2.rinterface_lib.sexp import NULLType
from rpy2.robjects import StrVector
from rpy2.robjects import globalenv as rpy2_globalenv
from rpy2.robjects import r as rpy2_r_interface
from rpy2.robjects.vectors import DataFrame as RDataFrame

from pysits.backend.functions import r_fnc_class, r_fnc_set_column
from pysits.backend.pkgs import r_pkg_arrow, r_pkg_base, r_pkg_sits


#
# Helper functions
#
def _load_arrow_table_reader_function() -> Callable[[str, list[str]], RDataFrame]:
    """Load and return an R function for reading Arrow tables with nested columns.

    This function defines and returns an R function that reads a Feather file and
    handles nested columns by unnesting them appropriately. The returned function
    takes a file path and a list of nested column names as arguments.

    Returns:
        Callable[[str, list[str]], RDataFrame]: An R function that takes a file path
            and list of nested column names as input and returns an R DataFrame with
            properly unnested columns.
    """
    rpy2_r_interface("""
        load_arrow_table <- function(path, nested_cols) {
            table <- arrow::read_feather(path)

            purrr::map_dfr(seq_len(nrow(table)), function(idx) {
                row_data <- table[idx,]

                for (col in nested_cols) {
                    row_nested <- row_data[[col]]
                    
                    # Handle arrow_list class
                    if (inherits(row_nested, "arrow_list")) {
                        row_nested <- lapply(row_nested, function(v) {
                            if (is.null(v)) return(NULL)
                            # Try to parse as JSON first
                            tryCatch({
                                parsed <- jsonlite::fromJSON(v)
                                setNames(as.character(parsed), names(parsed))
                            }, error = function(e) {
                                # If JSON parsing fails, return NULL
                                NULL
                            })
                        })
                        # If any values in row_nested are NULL, set the whole 
                        # thing to NULL
                        if (any(sapply(row_nested, is.null))) {
                            row_nested <- NULL
                        }
                    } else {
                        row_nested <- list(tidyr::unnest(
                            row_nested, 
                            cols = dplyr::everything()     
                        ))
                    }
                    
                    # Only create tibble if row_nested is not NULL
                    if (!is.null(row_nested)) {
                        row_data[[col]] <- NULL
                        row_data <- tibble::tibble(
                            row_data, 
                            !!col := row_nested
                        )
                    }
                }
                row_data
            })
        }
    """)

    return rpy2_globalenv["load_arrow_table"]


def _named_vector_to_json(x: RDataFrame, colname: str) -> RDataFrame:
    """Convert a named vector to a JSON string.

    Args:
        x (RDataFrame): R DataFrame containing a column with named vectors

        colname (str): Name of the column containing named vectors.

    Returns:
        RDataFrame: DataFrame with named vectors converted to JSON strings
    """
    # Define R code to convert named vector to JSON
    rpy2_r_interface(f"""
        named_vector_to_json <- function(x) {{
            vec_list <- lapply(x${colname}, function(v) {{
                if (is.null(names(v))) return(NULL)
                class(v) <- NULL
                json <- jsonlite::toJSON(as.list(setNames(as.character(v), names(v))), 
                                       auto_unbox=TRUE)
                class(json) <- NULL
                json
            }})
            x${colname} <- vec_list
            x
        }}
    """)

    # Call the R function and return result
    return rpy2_globalenv["named_vector_to_json"](x)


def _tibble_to_pandas_arrow(
    instance: RDataFrame,
    nested_columns: list[str] | None = None,
    table_processor: Callable[[RDataFrame], RDataFrame] | None = None,
) -> PandasDataFrame:
    """Convert an R DataFrame (tibble) to a Pandas DataFrame using Arrow format.

    This function handles the conversion of R DataFrames to Pandas DataFrames by:
    1. Creating a temporary Feather file
    2. Filtering out invalid columns (functions and NULL values)
    3. Writing valid columns to Feather format
    4. Reading back into Pandas
    5. Converting any nested columns to Pandas DataFrames

    Args:
        instance (RDataFrame): The R DataFrame (tibble) to convert.

        nested_columns (list[str] | None, optional): List of column names that
            contain nested data. Defaults to None.

    Returns:
        PandasDataFrame: The converted Pandas DataFrame.
    """
    # Create a temporary file
    tmp = tempfile.NamedTemporaryFile(suffix=".feather", delete=False)
    tmp_path = tmp.name
    tmp.close()

    # Extract columns from the data
    data_columns = r_pkg_base.colnames(instance)

    # Remove invalid columns
    data_columns_valid = []

    for data_column in data_columns:
        col = instance.rx2(data_column)

        # Remove invalid columns
        if r_fnc_class(col[0])[0] not in ["function", "NULL"]:
            data_columns_valid.append(data_column)

    # Select regular columns (using ``[]``) and convert to Pandas
    rdf_data = instance.rx(StrVector(data_columns_valid))

    # Process table
    if table_processor:
        rdf_data = table_processor(rdf_data)

    # Write to Feather format
    r_pkg_arrow.write_feather(rdf_data, tmp_path)

    # Read from Feather format
    df = feather.read_feather(tmp_path)

    # Convert nested columns to Pandas DataFrame
    if nested_columns:
        # Filter available columns
        nested_columns = [col for col in nested_columns if col in df.columns]

        # Convert nested columns to Pandas DataFrame
        for nested_column in nested_columns:
            df[nested_column] = df[nested_column].apply(
                lambda arr: PandasDataFrame.from_records(arr.tolist())
            )

    # Remove temporary file
    os.unlink(tmp_path)

    # Return value
    return df


def _pandas_to_tibble_arrow(
    instance: PandasDataFrame, nested_columns: list[str] | None = None
) -> RDataFrame:
    """Convert a Pandas DataFrame to an R DataFrame (tibble) using Arrow format.

    This function handles the conversion of Pandas DataFrames to R DataFrames by:
    1. Creating a temporary Feather file
    2. Converting nested columns to a format suitable for R
    3. Writing the data to Feather format
    4. Reading back into R using a custom Arrow table reader

    Args:
        instance (PandasDataFrame): The Pandas DataFrame to convert.

        nested_columns (list[str] | None, optional): List of column names that
            contain nested data. Defaults to None.

    Returns:
        RDataFrame: The converted R DataFrame (tibble).
    """
    instance = instance.copy(deep=True)

    tmp = tempfile.NamedTemporaryFile(suffix=".feather", delete=False)
    tmp_path = tmp.name
    tmp.close()

    # Convert nested columns to R DataFrame
    if nested_columns:
        # Filter available columns
        nested_columns = [col for col in nested_columns if col in instance.columns]

        # Convert nested columns to R DataFrame
        for nested_column in nested_columns:
            instance[nested_column] = instance[nested_column].apply(
                lambda arr: (
                    arr.to_dict(orient="list")
                    if isinstance(arr, PandasNDFrame)
                    else arr
                )
            )

    # Write to Feather
    feather.write_feather(instance, tmp_path)

    # Load Arrow table reader function
    load_arrow_table_fnc = _load_arrow_table_reader_function()

    # Read from Feather and unnest columns
    return load_arrow_table_fnc(tmp_path, nested_columns)


#
# General conversions
#
def tibble_nested_to_pandas_arrow(
    data: RDataFrame,
    nested_columns: list[str],
    table_processor: Callable[[RDataFrame], RDataFrame] | None = None,
) -> PandasDataFrame:
    """Convert any tibble to Pandas DataFrame.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: R Data Frame as Pandas.
    """
    return _tibble_to_pandas_arrow(data, nested_columns, table_processor)


def pandas_to_tibble_arrow(
    data: PandasDataFrame, nested_columns: list[str]
) -> RDataFrame:
    """Convert a pandas DataFrame to an R DataFrame object using Arrow.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.

    Returns:
        rpy2.robjects.vectors.DataFrame: The converted R DataFrame object.
    """
    return _pandas_to_tibble_arrow(data, nested_columns)


#
# SITS conversions function
#
def tibble_sits_to_pandas_arrow(data: RDataFrame) -> PandasDataFrame:
    """Convert sits tibble to Pandas DataFrame using Arrow.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.
    """
    # Define column order (from R)
    column_order = [
        "longitude",
        "latitude",
        "start_date",
        "end_date",
        "label",
        "cube",
        "time_series",
        "base_data",
        "predicted",
        "cluster",
        "id_sample",
        "id_neuron",
        "count",
    ]

    # Define nested columns
    nested_columns = ["time_series", "base_data", "predicted"]

    # Convert to Pandas DataFrame
    data_converted = tibble_nested_to_pandas_arrow(data, nested_columns)

    # Select columns
    columns_available = [v for v in column_order if v in data_converted.columns]

    # Return value
    return data_converted[columns_available]


def pandas_sits_to_tibble_arrow(data: PandasDataFrame) -> RDataFrame:
    """Convert sits pandas DataFrame to R DataFrame object using Arrow.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.
    """
    # Define nested columns
    nested_columns = ["time_series", "base_data", "predicted"]

    # Define data classes
    data_classes = ["sits", "tbl_df", "tbl", "data.frame"]

    if "predicted" in data.columns:
        data_classes.append("predicted")

    if "base_data" in data.columns:
        data_classes.append("sits_base")

    if "id_sample" in data.columns and "id_neuron" in data.columns:
        data_classes.append("som_clean_samples")

    # Convert to R DataFrame
    data = pandas_to_tibble_arrow(data, nested_columns)

    # Set class
    data.rclass = StrVector(data_classes)

    # Convert to R DataFrame
    return data


#
# Cube conversions function
#
def tibble_cube_to_pandas_arrow(data: RDataFrame) -> PandasDataFrame:
    """Convert sits tibble to Pandas DataFrame using Arrow.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.
    """
    # Define column order (from R)
    column_order = [
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
        "labels",
        "file_info",
        "vector_info",
        "base_info",
    ]

    # Define nested columns
    nested_columns = ["file_info", "vector_info"]

    # Define table processor
    def table_processor(x: RDataFrame) -> RDataFrame:
        """Process table."""

        # Process ``labels`` column
        if "labels" in x.colnames:
            # Get labels column
            labels = x.rx2("labels")

            # Check if labels have names
            labels_has_names = all(
                not isinstance(label.names, NULLType) for label in labels
            )

            # If labels have names, convert to JSON
            if labels_has_names:
                x = _named_vector_to_json(x, "labels")

        return x

    # Convert to Pandas DataFrame
    data_converted = tibble_nested_to_pandas_arrow(
        data, nested_columns, table_processor
    )

    # Process base_info separately if it exists
    if "base_info" in data.colnames:
        base_info = data.rx2("base_info")
        base_info_converted = []

        # Convert each base_info item to a cube if it's not None
        for i in range(len(base_info)):
            if not isinstance(base_info[i], NULLType):
                # Convert the base_info item to a cube
                base_info_converted.append(tibble_cube_to_pandas_arrow(base_info[i]))
            else:
                base_info_converted.append(None)

        # Add converted base_info to the DataFrame
        data_converted["base_info"] = base_info_converted

    # Select columns
    columns_available = [v for v in column_order if v in data_converted.columns]

    # Return value
    return data_converted[columns_available]


def pandas_cube_to_tibble_arrow(data: PandasDataFrame) -> RDataFrame:
    """Convert sits pandas DataFrame to R DataFrame object using Arrow.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.
    """
    # Define nested columns
    nested_columns = ["labels", "file_info", "vector_info"]

    # Handle base_info separately if it exists
    base_info = None

    if "base_info" in data.columns:
        # Convert base_info to R DataFrame
        base_info = pandas_cube_to_tibble_arrow(data.base_info)

        # Drop base_info from data
        data = data.drop(columns=["base_info"])

    # Convert to R DataFrame
    data = pandas_to_tibble_arrow(data, nested_columns)

    # Add base_info back if it exists
    if base_info is not None:
        data = r_fnc_set_column(data, "base_info", base_info)

    # Set class
    data.rclass = r_pkg_sits._cube_s3class(data)

    # Return value
    return data
