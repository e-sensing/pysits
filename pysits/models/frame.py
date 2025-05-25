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

"""frame models."""

import warnings

import numpy as np
from pandas import DataFrame as PandasDataFrame
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
    register_extension_dtype,
)


@register_extension_dtype
class SITSFrameDtype(ExtensionDtype):
    """SITS Frame dtype.

    Note:
        To learn more about the operations and attributes implemented on this class
        it is recommended to check the pandas documentation:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionDtype.html
    """

    name = "sits"
    """A string identifying the data type."""

    type = PandasDataFrame
    """The scalar type for the array."""

    kind = "O"
    """A character code (one of `biufcmMOSUV`) identifying the general kind of data.

    To learn more, please check: https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html
    """

    #
    # Class methods
    #
    @classmethod
    def construct_array_type(cls):
        return SITSFrameArray


class SITSFrameArray(ExtensionArray):
    """SITS Frame array type.

    Note:
        To learn more about the operations and attributes implemented on this class
        it is recommended to check the pandas documentation:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.extensions.ExtensionDtype.html
    """

    def __init__(self, frames):
        """Initializer."""
        self._data = frames

    #
    # Properties
    #
    @property
    def dtype(self):
        """Dtype value."""
        return SITSFrameDtype()

    #
    # Private methods
    #
    def _formatter(self, boxed=False):
        """Formatting function for scalar values."""
        return lambda x: f"NestedDataFrame(size = {len(x)})"

    #
    # Class methods
    #
    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        """Construct a new ExtensionArray from a sequence of scalars."""
        return cls(scalars)

    #
    # Dunder methods (magic methods)
    #
    def __getitem__(self, item):
        """Get item."""
        # Scalar `item` index
        if isinstance(item, int):
            return self._data[item]

        # Assuming `item` as a sequence
        frame_size = len(self._data)

        if isinstance(item, slice):
            # Safely handle ``slice`` start/stop/step
            indices = range(*item.indices(frame_size))

        else:
            # Assume it's iterable (like list or set)
            indices = item

        # Transform and return!
        return SITSFrameArray([self._data[idx] for idx in indices])

    def __len__(self):
        """Get object size."""
        return len(self._data)

    def __repr__(self):
        """Object representation."""
        return f"NestedDataFrame(size = {len(self._data)})"

    #
    # Operations
    #
    def take(self, indices, allow_fill=False, fill_value=None):
        """Take elements from an array."""
        with warnings.catch_warnings():
            # Ignoring pandas warning about non-standard input. This
            # will be solved soon
            warnings.simplefilter("ignore")

            # Take and return!
            return SITSFrameArray([self._data[idx] for idx in indices])

    def isna(self):
        """A 1-D array indicating if each value is missing."""
        return np.array([df is None for df in self._data])

    def copy(self):
        """Return a copy of the array."""
        return SITSFrameArray(self._data.copy())
