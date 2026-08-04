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

"""Xarray exporter."""

from functools import singledispatch

from pysits.docs import attach_doc
from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.frame import SITSFrame
from pysits.models.data.ts import SITSTimeSeriesModel

#
# Vector cubes
#
VECTOR_CUBE_CLASSES = (
    "vector_cube",
    "segs_cube",
    "probs_vector_cube",
    "class_vector_cube",
    "uncertainty_vector_cube",
    "variance_vector_cube",
)


@singledispatch
def _sits_as_xarray(data: SITSFrame, **kwargs):
    """sits as xarray dispatch."""
    raise NotImplementedError(
        f"There is no `sits_as_xarray` available for {type(data)}"
    )


@_sits_as_xarray.register
def _(data: SITSTimeSeriesModel, bands=None, scale=True, chunks=None, cube_args=None):
    """Convert time series to xarray."""
    from pysits.conversions.xarray import time_series_as_xarray

    # Time series are available in memory, so they are not read in chunks
    if chunks is not None or cube_args is not None:
        raise ValueError("`chunks` and `cube_args` are only available for data cubes.")

    # Load time-series
    return time_series_as_xarray(data, bands=bands)


@_sits_as_xarray.register
def _(data: SITSCubeModel, bands=None, scale=True, chunks=None, cube_args=None):
    """Convert a data cube to xarray."""
    from pysits.conversions.xarray import (
        derived_cube_as_xarray,
        raster_cube_as_xarray,
    )

    # Get cube classes
    cube_classes = list(data._instance.rclass)

    # Define if it is a vector cube
    is_vector_cube = [cls for cls in cube_classes if cls in VECTOR_CUBE_CLASSES]

    # If it is a vector cube, raise an error
    if is_vector_cube:
        raise NotImplementedError(
            f"There is no `sits_as_xarray` available for `{is_vector_cube[0]}`. "
            "Use `sits_as_geopandas` to export cubes with segments."
        )

    # Cubes derived from a classification have no time dimension
    if "derived_cube" in cube_classes:
        if bands is not None:
            raise ValueError(
                "`bands` is not available for cubes derived from a classification."
            )

        # Load derived cube
        return derived_cube_as_xarray(
            cube=data,
            scale=scale,
            chunks=chunks,
        )

    # Load raster cube
    return raster_cube_as_xarray(
        cube=data,
        bands=bands,
        scale=scale,
        chunks=chunks,
        cube_args=cube_args,
    )


@attach_doc("sits_as_xarray")
def sits_as_xarray(
    data: SITSFrame,
    *,
    bands: list[str] | None = None,
    scale: bool = True,
    chunks: dict | None = None,
    cube_args: dict | None = None,
):
    """Export a sits data object as an xarray object."""
    try:
        import pysits.conversions.xarray  # noqa: F401

    except ImportError as e:
        raise ImportError(
            "xarray dependencies not installed. To use this feature, please install "
            "them with `pip install pysits[xarray]`."
        ) from e

    return _sits_as_xarray(
        data,
        bands=bands,
        scale=scale,
        chunks=chunks,
        cube_args=cube_args,
    )
