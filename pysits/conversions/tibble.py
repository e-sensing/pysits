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

"""tibble conversions."""

import warnings
from collections.abc import Callable

from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from pandas import to_datetime as pandas_to_datetime
from rpy2 import robjects
from rpy2.robjects import StrVector, pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import DataFrame as RDataFrame
from shapely import wkt

from pysits.backend.functions import r_fnc_class
from pysits.backend.pkgs import r_pkg_base, r_pkg_sf
from pysits.models.frame import SITSFrameArray


#
# Auxiliary functions
#
def _column_to_datetime(data: PandasDataFrame, colname: str) -> PandasDataFrame:
    """Transform a columns from R to a valid datetime column in Python.

    Args:
        data (pandas.DataFrame): Pandas Data Frame from an R tibble/data.frame.

        colname (str): Column to be converted datetime (from R format to Python format).

    Returns:
        pandas.DataFrame: Pandas data frame with ``colname`` as datetime.
    """
    # Convert if column is available
    if colname in data.columns:
        data[colname] = pandas_to_datetime(data[colname], origin="1970-01-01", unit="D")

    # Return!
    return data


def _sf_to_shapely(sf_object: RDataFrame) -> list:
    """Transform a columns from R to a valid geometry column in Python.

    Args:
        sf_object (rpy2.robjects.vectors.ListVector): R (tibble/data.frame) Data frame.

    Returns:
        list: List of Shapely geometries.
    """
    # Extract geometry and convert to WKT in R directly
    geom_wkt = r_pkg_sf.st_as_text(r_pkg_sf.st_geometry(sf_object))

    # Convert R character vector to Python list of strings
    geom_wkt_py = list(geom_wkt)

    # Convert each WKT string to a Shapely geometry
    return [wkt.loads(g) for g in geom_wkt_py]


#
# Base conversion function
#
def _tibble_to_pandas(
    data: RDataFrame,
    nested_columns: list | None = None,
    table_processor: Callable[[PandasDataFrame], PandasDataFrame] | None = None,
    nested_processor: Callable[[PandasDataFrame], PandasDataFrame] | None = None,
) -> PandasDataFrame:
    """Convert an R tibble containing nested data frames to a Pandas DataFrame.

    Args:
        data (RDataFrame): An R tibble/data.frame object that contains
                           nested data frames.

        nested_columns (list): List of column names that contain nested
                               data frames.

        table_processor (Callable | None, optional):
            A function to process the main table after conversion. The function should
            take a pandas DataFrame as input and return a processed pandas DataFrame.
            Defaults to None.

        nested_processor (Callable | None, optional):
            A function to process each nested data frame after conversion. The function
            should take a pandas DataFrame as input and return a processed pandas
            DataFrame. Defaults to None.

    Returns:
        PandasDataFrame: A pandas DataFrame where the nested columns are converted to
                         SITSFrameArray objects containing the processed nested
                         data frames.
    """
    # Check if the data is an SF object
    has_geometries = "sf" in r_fnc_class(data)

    # Define shapely geometries and CRS
    shapely_crs = None
    shapely_geometries = None

    # Handle SF objects
    if has_geometries:
        # Convert geometry to Shapely geometries
        shapely_geometries = _sf_to_shapely(data)

        # Get CRS
        shapely_crs = r_pkg_sf.st_crs(data)

        # Check if CRS is available
        if "NULL" not in r_fnc_class(shapely_crs):
            shapely_crs = shapely_crs.rx2("wkt")[0]

        # Drop geometry column
        data = r_pkg_sf.st_drop_geometry(data)

    # Convert columns definitions
    nested_columns = nested_columns if nested_columns else []

    # Extract columns from the data
    data_columns = r_pkg_base.colnames(data)

    # Remove invalid columns
    data_columns_valid = []

    for data_column in data_columns:
        col = data.rx2(data_column)

        # Remove invalid columns
        if r_fnc_class(col[0])[0] not in ["function", "NULL"]:
            data_columns_valid.append(data_column)

    # Replace old data columns with the filtered one
    data_columns = data_columns_valid

    # If user define nested columns, verify if they are available.
    if nested_columns:
        # Filter available nested columns
        nested_columns = [v for v in nested_columns if v in data_columns]

        # If selected columns are available, remove them from the data columns
        # This allows us to handle them individually.
        if nested_columns:
            data_columns = list(set(data_columns).difference(nested_columns))

    # Select regular columns (using ``[]``) and convert to Pandas
    rdf_data = data.rx(StrVector(data_columns))
    rdf_data = pandas2ri.rpy2py(rdf_data)

    # Handle nested columns if available
    for nested_column in nested_columns:
        # Select nested column (using ``[[]]``)
        nested_column_data = data.rx2(nested_column)

        # As it is a nested column, handle it as a list of ``tibble/data.frame``
        nested_column_processed = []

        for nested_row in nested_column_data:
            # Convert to pandas
            nested_row_df = pandas2ri.rpy2py(nested_row)

            # If a processor function is available, apply data to use
            if nested_processor and isinstance(nested_row_df, PandasDataFrame):
                nested_row_df = nested_processor(nested_row_df)

            # Save
            nested_column_processed.append(nested_row_df)

        # Convert column to SITS Array and save to the main data frame
        rdf_data[nested_column] = SITSFrameArray(nested_column_processed)

    # If a processor function is available to the main table, use it
    if table_processor:
        rdf_data = table_processor(rdf_data)

    # Transform dataframe to geodataframe
    if shapely_geometries:
        rdf_data = GeoPandasDataFrame(
            rdf_data, geometry=shapely_geometries, crs=shapely_crs
        )

    # Return!
    return rdf_data


#
# General function
#
def tibble_to_pandas(data: RDataFrame) -> PandasDataFrame:
    """Convert any tibble to Pandas DataFrame.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: R Data Frame as Pandas.
    """

    # Define table processor
    def _table_processor(x):
        """Table processor."""
        # Update date columns
        x = _column_to_datetime(x, "start_date")
        x = _column_to_datetime(x, "end_date")

        return x

    # Convert and return
    return _tibble_to_pandas(
        data=data,
        table_processor=_table_processor,
    )


def tibble_nested_to_pandas(
    data: RDataFrame,
    nested_columns: list,
    table_processor: Callable[[PandasDataFrame], PandasDataFrame] | None = None,
    nested_processor: Callable[[PandasDataFrame], PandasDataFrame] | None = None,
) -> PandasDataFrame:
    """(Public) Convert an R tibble containing nested data frames to a Pandas DataFrame.

    Args:
        data (RDataFrame): An R tibble/data.frame object that contains
                           nested data frames.

        nested_columns (list): List of column names that contain nested
                               data frames.

        table_processor (Callable | None, optional):
            A function to process the main table after conversion. The function should
            take a pandas DataFrame as input and return a processed pandas DataFrame.
            Defaults to None.

        nested_processor (Callable | None, optional):
            A function to process each nested data frame after conversion. The function
            should take a pandas DataFrame as input and return a processed pandas
            DataFrame. Defaults to None.

    Returns:
        PandasDataFrame: A pandas DataFrame where the nested columns are converted to
                         SITSFrameArray objects containing the processed nested
                         data frames.
    """
    return _tibble_to_pandas(
        data=data,
        nested_columns=nested_columns,
        table_processor=table_processor,
        nested_processor=nested_processor,
    )


#
# SITS conversions function
#
def tibble_sits_to_pandas(data: RDataFrame) -> PandasDataFrame:
    """Convert sits tibble to Pandas Data Frame.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: R Data Frame as Pandas.
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
    ]

    # Define nested columns
    nested_columns = ["time_series", "predicted"]

    # Define table processor
    def _table_processor(x):
        """Table processor."""
        # Update date columns
        x = _column_to_datetime(x, "start_date")
        x = _column_to_datetime(x, "end_date")

        x_columns = list(filter(lambda y: y in x.columns, column_order))
        x_columns = x_columns + list(set(x.columns).difference(x_columns))

        return x[x_columns]

    # Define nested processor
    def _nested_processor(x):
        """Nested processor."""
        return _column_to_datetime(x, "Index")

    # Convert and return
    return _tibble_to_pandas(
        data=data,
        nested_columns=nested_columns,
        table_processor=_table_processor,
        nested_processor=_nested_processor,
    )


#
# Cube conversions function
#
def tibble_cube_to_pandas(data: RDataFrame) -> PandasDataFrame:
    """Convert sits tibble to Pandas Data Frame.

    Args:
        data (rpy2.robjects.vectors.DataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: R Data Frame as Pandas.
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
    ]

    # Define nested columns
    nested_columns = ["labels", "file_info", "vector_info"]

    # Define table processor
    def _table_processor(x):
        """Table processor."""
        columns_available = [v for v in column_order if v in x.columns]

        return x[columns_available]

    # Define nested processor
    def _nested_processor(x):
        """Nested processor."""
        x = _column_to_datetime(x, "date")
        x = _column_to_datetime(x, "start_date")
        x = _column_to_datetime(x, "end_date")

        return x

    # Convert and return
    return _tibble_to_pandas(
        data=data,
        nested_columns=nested_columns,
        table_processor=_table_processor,
        nested_processor=_nested_processor,
    )


#
# Pandas to R conversions
#
def pandas_to_tibble(data: PandasDataFrame) -> RDataFrame:
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


def geopandas_to_tibble(data: GeoPandasDataFrame) -> RDataFrame:
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
