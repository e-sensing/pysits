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

from pysits.models.data.cube import SITSCubeModel
from pysits.models.data.frame import SITSFrame
from pysits.models.data.ts import SITSTimeSeriesModel


@singledispatch
def _sits_as_xarray(data: SITSFrame):
    """sits as xarray dispatch."""
    raise NotImplementedError(
        f"There is no `sits_as_xarray` available for {type(data)}"
    )


@_sits_as_xarray.register
def _(data: SITSTimeSeriesModel):
    """Convert sits to xarray."""
    from pysits.conversions.xarray import pandas_sits_as_xarray

    return pandas_sits_as_xarray(data)


@_sits_as_xarray.register
def _(data: SITSCubeModel):
    """Convert cube to xarray."""
    from pysits.conversions.xarray import pandas_cube_as_xarray

    return pandas_cube_as_xarray(data)


def sits_as_xarray(data: SITSFrame):
    """Convert data to xarray."""
    try:
        from pysits.conversions.xarray import (
            pandas_cube_as_xarray,  # noqa
            pandas_sits_as_xarray,  # noqa
        )

    except ImportError as e:
        raise ImportError(
            "xarray dependencies not installed. To use this feature, please install "
            "them with `pip install pysits[xarray]`."
        ) from e

    return _sits_as_xarray(data)
