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

"""Apply operations."""

import rpy2.robjects as ro

from pysits.backend.functions import r_fnc_class
from pysits.conversions.base import rpy2_fix_type
from pysits.docs import attach_doc
from pysits.models import SITSCubeModel, SITSFrame, SITSTimeSeriesModel


#
# Utilities
#
def _class_selector(data) -> type[SITSFrame]:
    """Selects the appropriate class for the given data.

    Args:
        data (r object): the data to select the class for.

    Returns:
        type[SITSFrame]: Specialized SITS model.
    """
    cls = SITSTimeSeriesModel

    if "raster_cube" in r_fnc_class(data):
        cls = SITSCubeModel

    return cls


#
# Apply operation
#
@rpy2_fix_type
@attach_doc("sits_apply")
def sits_apply(data, **kwargs) -> SITSFrame:
    """Apply a function on a set of time series."""
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
