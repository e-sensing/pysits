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

import io
import warnings
from collections.abc import Callable

import pyarrow as pa
import pyarrow.ipc
from geopandas import GeoDataFrame as GeoPandasDataFrame
from pandas import DataFrame as PandasDataFrame
from pandas import to_datetime as pandas_to_datetime
from pandas.core.generic import NDFrame as PandasNDFrame
from rpy2 import robjects
from rpy2.rinterface_lib.sexp import NULLType
from rpy2.robjects import StrVector, pandas2ri
from rpy2.robjects import globalenv as rpy2_globalenv
from rpy2.robjects import r as rpy2_r_interface
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.vectors import DataFrame as RDataFrame
from shapely import wkt

from pysits.backend.functions import r_fnc_class, r_fnc_set_column
from pysits.backend.pkgs import r_pkg_base, r_pkg_sf, r_pkg_sits
from pysits.models.frame import NestedFrame


#
# Auxiliary functions
#
def _column_to_datetime(data: PandasDataFrame, colname: str) -> PandasDataFrame:
    """Transform a column from R to a valid datetime column in Python.

    Handles both R integer date offsets (days since 1970-01-01) and
    columns already converted to datetime by Arrow IPC.

    Args:
        data (pandas.DataFrame): Pandas Data Frame from an R tibble/data.frame.

        colname (str): Column to be converted datetime (from R format to Python format).

    Returns:
        pandas.DataFrame: Pandas data frame with ``colname`` as datetime.
    """
    if colname in data.columns:
        col = data[colname]

        if hasattr(col.dtype, "kind") and col.dtype.kind in ("i", "f"):
            # R integer/float date offsets — convert from days since epoch
            data[colname] = pandas_to_datetime(col, origin="1970-01-01", unit="D")

        else:
            # Already date/datetime or string — just ensure datetime type
            data[colname] = pandas_to_datetime(col)

    return data


def _sf_to_shapely(sf_object: RDataFrame) -> list:
    """Transform R sf geometries to Shapely geometries via WKT.

    Args:
        sf_object (rpy2.robjects.vectors.DataFrame): R sf data frame.

    Returns:
        list: List of Shapely geometries.
    """
    geom_wkt = r_pkg_sf.st_as_text(r_pkg_sf.st_geometry(sf_object))
    geom_wkt_py = list(geom_wkt)

    return [wkt.loads(g) for g in geom_wkt_py]


#
# Arrow IPC helpers
#
def _ensure_r_ipc_functions():
    """Define R-side IPC reader/writer/unnester functions once."""
    if "pysits_write_ipc_raw" in rpy2_globalenv:
        return

    rpy2_r_interface("""
        pysits_write_ipc_raw <- function(df) {
            tf <- tempfile(fileext = ".arrows")

            on.exit(unlink(tf))
            arrow::write_ipc_stream(df, tf)

            readBin(tf, "raw", file.info(tf)$size)
        }

        pysits_read_ipc_raw <- function(raw_bytes) {
            tf <- tempfile(fileext = ".arrows")

            on.exit(unlink(tf))
            writeBin(raw_bytes, tf)

            as.data.frame(arrow::read_ipc_stream(tf))
        }

        pysits_read_and_unnest <- function(raw_bytes, nested_cols) {
            table <- pysits_read_ipc_raw(raw_bytes)

            purrr::map_dfr(seq_len(nrow(table)), function(idx) {
                row_data <- table[idx,]

                for (col in nested_cols) {
                    row_nested <- row_data[[col]]

                    # Handle arrow_list class
                    if (inherits(row_nested, "arrow_list")) {
                        row_nested <- lapply(row_nested, function(v) {
                            if (is.null(v)) {
                                return(NULL)
                            }

                            tryCatch({
                                parsed <- jsonlite::fromJSON(v)
                                setNames(as.character(parsed), names(parsed))
                            }, error = function(e) {
                                NULL
                            })
                        })

                        if (any(sapply(row_nested, is.null))) {
                            row_nested <- NULL
                        }
                    } else {
                        row_nested <- list(tidyr::unnest(
                            row_nested,
                            cols = dplyr::everything()
                        ))
                    }

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


def _dataframe_to_ipc_bytes(df: PandasDataFrame) -> bytes:
    """Serialize a pandas DataFrame to Arrow IPC bytes.

    Args:
        df (pandas.DataFrame): DataFrame to serialize.

    Returns:
        bytes: Arrow IPC stream bytes.
    """
    table = pa.Table.from_pandas(df)
    sink = io.BytesIO()

    writer = pa.ipc.new_stream(sink, table.schema)
    writer.write_table(table)
    writer.close()

    return sink.getvalue()


def _ipc_bytes_to_dataframe(raw_bytes: bytes) -> PandasDataFrame:
    """Deserialize Arrow IPC bytes to a pandas DataFrame.

    Args:
        raw_bytes (bytes): Arrow IPC stream bytes.

    Returns:
        pandas.DataFrame: Deserialized DataFrame.
    """
    reader = pa.ipc.open_stream(raw_bytes)

    return reader.read_pandas()


def _named_vector_to_json(x: RDataFrame, colname: str) -> RDataFrame:
    """Convert a named vector column to JSON strings.

    Args:
        x (RDataFrame): R DataFrame containing a column with named vectors.

        colname (str): Name of the column containing named vectors.

    Returns:
        RDataFrame: DataFrame with named vectors converted to JSON strings.
    """
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

    return rpy2_globalenv["named_vector_to_json"](x)


#
# Core R-to-Python conversion
#
def _tibble_to_pandas(  # noqa: PLR0912
    data: RDataFrame,
    nested_columns: list | None = None,
    table_processor: Callable | None = None,
    nested_processor: Callable[[PandasDataFrame], PandasDataFrame] | None = None,
) -> PandasDataFrame:
    """Convert an R tibble to a Pandas DataFrame using Arrow IPC.

    Args:
        data (RDataFrame): An R tibble/data.frame object.

        nested_columns (list | None): Column names containing nested data frames.

        table_processor (Callable | None): Function to process the R data before
            Arrow transfer. Receives and returns an RDataFrame.

        nested_processor (Callable | None): Function to process each nested
            pandas DataFrame after conversion.

    Returns:
        PandasDataFrame: Converted DataFrame with nested columns as NestedFrame.
    """
    _ensure_r_ipc_functions()

    # Check if the data is an SF object
    has_geometries = "sf" in r_fnc_class(data)

    shapely_crs = None
    shapely_geometries = None

    if has_geometries:
        shapely_geometries = _sf_to_shapely(data)
        shapely_crs = r_pkg_sf.st_crs(data)

        if "NULL" not in r_fnc_class(shapely_crs):
            shapely_crs = shapely_crs.rx2("wkt")[0]

        data = r_pkg_sf.st_drop_geometry(data)

    nested_columns = nested_columns if nested_columns else []

    # Extract and filter valid columns
    data_columns = r_pkg_base.colnames(data)
    data_columns_valid = []

    for data_column in data_columns:
        col = data.rx2(data_column)

        if r_fnc_class(col[0])[0] not in ["function", "NULL"]:
            data_columns_valid.append(data_column)

    data_columns = data_columns_valid

    # Separate nested columns from regular columns
    if nested_columns:
        nested_columns = [v for v in nested_columns if v in data_columns]

        if nested_columns:
            data_columns = list(set(data_columns).difference(nested_columns))

    # Select regular columns
    rdf_data = data.rx(StrVector(data_columns))

    # Apply table processor on R side before transfer
    if table_processor:
        rdf_data = table_processor(rdf_data)

    # Transfer regular columns via IPC
    r_write_fnc = rpy2_globalenv["pysits_write_ipc_raw"]
    raw_bytes = bytes(r_write_fnc(rdf_data))
    result_df = _ipc_bytes_to_dataframe(raw_bytes)

    # Handle nested columns
    for nested_column in nested_columns:
        nested_column_data = data.rx2(nested_column)
        nested_column_processed = []

        for nested_row in nested_column_data:
            # Convert each nested tibble via IPC
            try:
                nested_raw = bytes(r_write_fnc(nested_row))
                nested_row_df = NestedFrame(_ipc_bytes_to_dataframe(nested_raw))

            except Exception:
                # Fallback to rpy2 conversion for non-standard nested data
                nested_row_df = pandas2ri.rpy2py(nested_row)

                if isinstance(nested_row_df, PandasDataFrame):
                    nested_row_df = NestedFrame(nested_row_df)

            if nested_processor and isinstance(nested_row_df, PandasDataFrame):
                nested_row_df = NestedFrame(nested_processor(nested_row_df))

            nested_column_processed.append(nested_row_df)

        result_df[nested_column] = nested_column_processed

    # Transform to GeoDataFrame if SF
    if shapely_geometries:
        result_df = GeoPandasDataFrame(
            result_df, geometry=shapely_geometries, crs=shapely_crs
        )

    return result_df


#
# Core Python-to-R conversion
#
def _pandas_to_tibble(
    instance: PandasDataFrame, nested_columns: list[str] | None = None
) -> RDataFrame:
    """Convert a Pandas DataFrame to an R tibble using Arrow IPC.

    Args:
        instance (PandasDataFrame): The Pandas DataFrame to convert.

        nested_columns (list[str] | None): Column names containing nested DataFrames.

    Returns:
        RDataFrame: The converted R DataFrame (tibble).
    """
    _ensure_r_ipc_functions()

    instance = instance.copy(deep=True)

    # Convert nested columns to dict-of-lists for Arrow serialization
    if nested_columns:
        nested_columns = [col for col in nested_columns if col in instance.columns]

        for nested_column in nested_columns:
            instance[nested_column] = instance[nested_column].apply(
                lambda arr: (
                    arr.to_dict(orient="list")
                    if isinstance(arr, PandasNDFrame)
                    else arr
                )
            )

    # Serialize to IPC bytes
    ipc_bytes = _dataframe_to_ipc_bytes(instance)

    # Transfer to R as raw vector
    r_raw = robjects.vectors.ByteVector(ipc_bytes)

    if nested_columns:
        # Read and unnest in R
        r_unnest_fnc = rpy2_globalenv["pysits_read_and_unnest"]

        return r_unnest_fnc(r_raw, StrVector(nested_columns))

    else:
        # Simple read in R
        r_read_fnc = rpy2_globalenv["pysits_read_ipc_raw"]

        return r_read_fnc(r_raw)


#
# Public API — General
#
def tibble_to_pandas(data: RDataFrame) -> PandasDataFrame:
    """Convert any tibble to Pandas DataFrame.

    Args:
        data (RDataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: R Data Frame as Pandas.
    """

    def _table_processor(x):
        """Process date columns on R side (no-op; dates handled after IPC)."""
        return x

    result = _tibble_to_pandas(data=data, table_processor=_table_processor)
    result = _column_to_datetime(result, "start_date")
    result = _column_to_datetime(result, "end_date")

    return result


def tibble_nested_to_pandas(
    data: RDataFrame,
    nested_columns: list,
    table_processor: Callable | None = None,
    nested_processor: Callable[[PandasDataFrame], PandasDataFrame] | None = None,
) -> PandasDataFrame:
    """Convert an R tibble with nested data frames to a Pandas DataFrame.

    Args:
        data (RDataFrame): An R tibble/data.frame with nested data frames.

        nested_columns (list): Column names containing nested data frames.

        table_processor (Callable | None): Function to process the R data.

        nested_processor (Callable | None): Function to process nested DataFrames.

    Returns:
        PandasDataFrame: Converted DataFrame with nested columns.
    """
    return _tibble_to_pandas(
        data=data,
        nested_columns=nested_columns,
        table_processor=table_processor,
        nested_processor=nested_processor,
    )


def pandas_to_tibble(data: PandasDataFrame) -> RDataFrame:
    """Convert a pandas DataFrame to an R DataFrame.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.

    Returns:
        rpy2.robjects.vectors.DataFrame: The converted R DataFrame object.
    """
    with localconverter(robjects.default_converter + pandas2ri.converter):
        return robjects.conversion.py2rpy(data)


def geopandas_to_tibble(data: GeoPandasDataFrame) -> RDataFrame:
    """Convert a GeoPandas GeoDataFrame to an R sf object.

    Removes columns that contain embedded DataFrames (NestedFrame).
    """
    data = GeoPandasDataFrame(data)

    if data.crs is None:
        raise ValueError("GeoDataFrame must have a CRS")

    # Identify columns where no cell is a NestedFrame
    safe_columns = []
    for col in data.columns:
        if data[col].dtype == object:
            first_valid = (
                data[col].dropna().iloc[0] if not data[col].dropna().empty else None
            )

            if isinstance(first_valid, PandasDataFrame):
                continue

        safe_columns.append(col)

    dropped_columns = set(data.columns) - set(safe_columns)
    if dropped_columns:
        warnings.warn(
            f"Warning: Dropping columns with embedded DataFrames: {dropped_columns}"
        )

    data_safe = data[safe_columns].copy()

    if isinstance(data, GeoPandasDataFrame):
        geom_col = data.geometry.name
        data_safe[geom_col] = data.geometry.to_wkt()

    with localconverter(robjects.default_converter + pandas2ri.converter):
        r_df = robjects.conversion.py2rpy(data_safe)

    if isinstance(data, GeoPandasDataFrame):
        r_df = r_pkg_sf.st_as_sf(
            r_df,
            wkt=robjects.StrVector([geom_col]),
            crs=robjects.StrVector([data.crs.to_wkt()]),
        )

    return r_df


#
# Public API — SITS-specific
#
def tibble_sits_to_pandas(data: RDataFrame) -> PandasDataFrame:
    """Convert a sits tibble to Pandas DataFrame.

    Args:
        data (RDataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: Converted sits DataFrame.
    """
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

    nested_columns = [
        "time_series",
        "base_data",
        "predicted",
    ]

    def _nested_processor(x):
        return _column_to_datetime(x, "Index")

    result = _tibble_to_pandas(
        data=data,
        nested_columns=nested_columns,
        nested_processor=_nested_processor,
    )

    # Apply datetime conversions
    result = _column_to_datetime(result, "start_date")
    result = _column_to_datetime(result, "end_date")

    # Order columns
    columns_available = [v for v in column_order if v in result.columns]
    columns_available = columns_available + list(
        set(result.columns).difference(columns_available)
    )

    return result[columns_available]


def pandas_sits_to_tibble(data: PandasDataFrame) -> RDataFrame:
    """Convert a sits pandas DataFrame to R tibble.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.

    Returns:
        rpy2.robjects.vectors.DataFrame: The converted R DataFrame.
    """
    nested_columns = [
        "time_series",
        "base_data",
        "predicted",
    ]

    data_classes = [
        "sits",
        "tbl_df",
        "tbl",
        "data.frame",
    ]

    if "predicted" in data.columns:
        data_classes.append("predicted")

    if "base_data" in data.columns:
        data_classes.append("sits_base")

    if "id_sample" in data.columns and "id_neuron" in data.columns:
        data_classes.append("som_clean_samples")

    data = _pandas_to_tibble(data, nested_columns)
    data.rclass = StrVector(data_classes)

    return data


#
# Public API — Cube-specific
#
def tibble_cube_to_pandas(data: RDataFrame) -> PandasDataFrame:
    """Convert a sits cube tibble to Pandas DataFrame.

    Args:
        data (RDataFrame): R (tibble/data.frame) Data frame.

    Returns:
        pandas.DataFrame: Converted cube DataFrame.
    """
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

    nested_columns = [
        "file_info",
        "vector_info",
    ]

    def table_processor(x: RDataFrame) -> RDataFrame:
        if "labels" in x.colnames:
            labels = x.rx2("labels")
            labels_has_names = all(
                not isinstance(label.names, NULLType) for label in labels
            )

            if labels_has_names:
                return _named_vector_to_json(x, "labels")

        return x

    data_converted = _tibble_to_pandas(data, nested_columns, table_processor)

    # Process base_info separately if it exists (recursive)
    if "base_info" in data.colnames:
        base_info = data.rx2("base_info")
        base_info_converted = []

        for i in range(len(base_info)):
            if not isinstance(base_info[i], NULLType):
                base_info_converted.append(tibble_cube_to_pandas(base_info[i]))

            else:
                base_info_converted.append(None)

        data_converted["base_info"] = base_info_converted

    columns_available = [v for v in column_order if v in data_converted.columns]

    return data_converted[columns_available]


def pandas_cube_to_tibble(data: PandasDataFrame) -> RDataFrame:
    """Convert a cube pandas DataFrame to R tibble.

    Args:
        data (pandas.DataFrame): The pandas DataFrame to convert to R.

    Returns:
        rpy2.robjects.vectors.DataFrame: The converted R DataFrame.
    """
    nested_columns = [
        "labels",
        "file_info",
        "vector_info",
    ]

    base_info = None
    if "base_info" in data.columns:
        base_info = pandas_cube_to_tibble(data.base_info)
        data = data.drop(columns=["base_info"])

    data = _pandas_to_tibble(data, nested_columns)

    if base_info is not None:
        data = r_fnc_set_column(data, "base_info", base_info)

    data.rclass = r_pkg_sits._cube_s3class(data)

    return data
