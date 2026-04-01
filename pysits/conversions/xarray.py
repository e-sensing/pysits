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

"""Xarray conversions."""

from __future__ import annotations

import dask.array as dask_array
import numpy as np
import rioxarray as xrio
import xarray as xr
from affine import Affine
from pandas import concat as pandas_concat
from pandas import to_datetime as pandas_to_datetime

from pysits.models.data.base import SITSData


#
# Auxiliary functions
#
def _xarray_load_raster(
    raster_path: str,
    crs: str,
    shape: tuple[int, int],
    transform: float,
    chunks=None,
    dtype=None,
) -> xr.DataArray:
    """Load raster with rio-xarray.

    Args:
        raster_path (str): Complete path to the raster.

        crs (str): Dataset CRS.

        shape (Tuple[int, int]): Dataset shape.

        transform (float): Project transform.

        chunks: Dask chunk specification. If None, loads eagerly. If not None,
            wraps the load+reproject in ``dask.delayed`` (one chunk per file) so the
            computation graph stays deferred until ``.compute()`` is called.
            Note: ``rio.reproject`` always materialises internally; laziness is
            achieved by deferring the entire operation as a single dask task.

        dtype: NumPy dtype for the lazy dask array. Only used when chunks is not None.

    Returns:
        xr.DataArray: Raster loaded as DataArray
    """
    if chunks is not None:
        import dask

        height, width = shape

        def _load() -> np.ndarray:
            # Load raster with rio-xarray
            _da = xrio.open_rasterio(raster_path, masked=True)
            _da = _da.squeeze("band", drop=True)

            # Reproject raster
            return _da.rio.reproject(
                dst_crs=crs, shape=shape, transform=transform, resampling=0
            ).values

        # Wrap with dask
        lazy_values = dask_array.from_delayed(
            dask.delayed(_load)(),
            shape=(height, width),
            dtype=dtype if dtype is not None else np.float32,
        )

        # Calculate coordinates
        x_coords = transform.c + (np.arange(width) + 0.5) * transform.a
        y_coords = transform.f + (np.arange(height) + 0.5) * transform.e

        # Create xarray DataArray
        return xr.DataArray(
            lazy_values, dims=["y", "x"], coords={"x": x_coords, "y": y_coords}
        )

    # Load raster with rio-xarray
    da = xrio.open_rasterio(raster_path, masked=True)

    # Squeeze band dimension
    da = da.squeeze("band", drop=True)

    # Reproject raster
    return da.rio.reproject(
        dst_crs=crs,
        shape=shape,
        transform=transform,
        # resampling=0,  # 0 = Nearest
    )


#
# SITS conversions function
#
def pandas_sits_as_xarray(data: SITSData, chunks=None) -> xr.Dataset:
    """Convert sits to xarray.

    Args:
        data (pysits.models.SITSData): SITS Data.

        chunks: Dask chunk specification. If None (default), data is kept as a numpy
            array. If provided, wraps the array with dask for lazy graph-based
            downstream operations.

    Returns:
        xr.Dataset: SITS data as xarray.Dataset.
    """
    # Metadata columns
    time_series_metadata = data.drop(columns="time_series")

    # Extract time-series column
    time_series_data = data["time_series"]

    # Convert to a list of data frames
    time_series_data = time_series_data.tolist()

    # Get time-series attributes (removing ``Index``)
    time_series_attributes = set(time_series_data[0].columns).difference(["Index"])
    time_series_attributes = list(time_series_attributes)

    # Extract samples timeline
    timeline = time_series_data[0]["Index"]

    # Drop ``Index`` and create a stack
    time_series_np = np.stack(
        [ts.drop(columns="Index").to_numpy() for ts in time_series_data]
    )

    # Optionally wrap with dask
    if chunks is not None:
        time_series_data = dask_array.from_array(time_series_np, chunks=chunks)

    else:
        time_series_data = time_series_np

    # Create xarray dataset
    return xr.Dataset(
        data_vars={
            var: (["sample", "time"], time_series_data[:, :, i])
            for i, var in enumerate(time_series_attributes)
        },
        coords={
            "sample": np.arange(len(time_series_metadata)),
            "time": timeline,
            "longitude": ("sample", time_series_metadata["longitude"].to_numpy()),
            "latitude": ("sample", time_series_metadata["latitude"].to_numpy()),
            "label": ("sample", time_series_metadata["label"].to_numpy()),
            "cube": ("sample", time_series_metadata["cube"].to_numpy()),
        },
    )


def pandas_cube_as_xarray(cube: SITSData, chunks="auto") -> xr.Dataset:
    """Convert cube to xarray.

    Args:
        cube (pysits.models.SITSData): Cube data

        chunks: Dask chunk specification passed to ``open_rasterio``. Defaults to
            "auto", which lets dask size chunks based on available memory. Pass None
            to load eagerly, or a dict such as ``{"x": 512, "y": 512}`` for fixed
            spatial tiles.

    Returns:
        xr.Dataset: Cube data as xarray.Dataset.
    """
    # Get all files from the cube
    cube_file_info = cube["file_info"].tolist()

    # Merge and sort values
    cube_file_info = pandas_concat(cube_file_info, ignore_index=True)
    cube_file_info = cube_file_info.sort_values(["date", "band"]).reset_index(drop=True)

    # Assuming all cube have the same CRS / resolution, use one file
    # to extract ``shape``, ``coords``, ``crs``, and ``dtype`` (no pixel data read)
    cube_sample = xrio.open_rasterio(cube_file_info.iloc[0]["path"], masked=True)

    # Extract info
    cube_crs = cube_sample.rio.crs
    cube_dtype = cube_sample.dtype
    cube_res_x, cube_res_y = [abs(x) for x in cube_sample.rio.resolution()]

    # To handle multiple tiles, use a ``global`` extent, covering all tiles
    xmin = cube_file_info["xmin"].min()
    xmax = cube_file_info["xmax"].max()
    ymin = cube_file_info["ymin"].min()
    ymax = cube_file_info["ymax"].max()

    # Calculate global shape
    width = int(np.ceil((xmax - xmin) / cube_res_x))
    height = int(np.ceil((ymax - ymin) / cube_res_y))

    # Define global transform
    global_transform = Affine.translation(xmin, ymax) * Affine.scale(
        cube_res_x, -cube_res_y
    )

    # Build per-band DataArrays using xr.concat (lazy-safe)
    band_arrays = []

    for band, band_data in cube_file_info.groupby("band"):
        time_slices = []

        for _, row in band_data.sort_values("date").iterrows():
            # Load raster using rio-xarray
            da = _xarray_load_raster(
                raster_path=row["path"],
                crs=cube_crs,
                shape=(height, width),
                transform=global_transform,
                chunks=chunks,
                dtype=cube_dtype,
            )

            da = da.expand_dims({"time": [pandas_to_datetime(row["date"])]})
            time_slices.append(da)

        band_da = xr.concat(time_slices, dim="time").rename(band)
        band_arrays.append(band_da)

    ds = xr.merge(band_arrays)

    # Save CRS
    ds.rio.write_crs(cube_crs, inplace=True)

    return ds
