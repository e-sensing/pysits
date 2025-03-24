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

"""segment operations."""

import rpy2.robjects as ro

from pysits import types as type_utils
from pysits.backend.utils import r_class
from pysits.models import SITSCubeModel, SITSTimeSeriesModel


#
# Utilities
#
def _class_selector(data):
    """Selects the appropriate class for the given data.

    Args:
        data (r object): the data to select the class for.

    Returns:
        SITSModel: Specialized SITS model.
    """
    cls = SITSTimeSeriesModel

    if "raster_cube" in r_class(data):
        cls = SITSCubeModel

    return cls


#
# Apply operation
#
@type_utils.rpy2_fix_type
def sits_apply(data, **kwargs):
    """Apply a function on a set of time series.

    Apply a named expression to a sits cube or a sits tibble to be
    evaluated and generate new bands (indices). In the case of sits cubes,
    it materializes a new band in output_dir using gdalcubes.
    """
    params = []

    # Process parameters manually
    for k, v in kwargs.items():
        current_v = v[0]

        if k == "output_dir":
            current_v = f"'{current_v}'"

        params.append(f"{k}={current_v}")

    # Build the ``sits_apply`` command manually to support
    # high-level expression definition (using string)
    command = f"""
        sits_apply(
            {data.r_repr()},
            {", ".join(params)}
        )
    """

    # Run operation
    result = ro.r(command)

    # Define class
    cls = _class_selector(result)

    return cls(result)
