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

"""time series operations."""

from pysits.backend.sits import r_sits
from pysits.models import SITSOMData, SITSPredictors, SITSTimeSeriesModel
from pysits.toolbox.conversions.base import rpy2_fix_type


#
# High-level operation
#
@rpy2_fix_type
def sits_get_data(*args, **kwargs):
    """Retrieve time series data from a data cube.

    Retrieve a set of time series from a data cube or from a time series service.
    """
    data = r_sits.sits_get_data(*args, **kwargs)

    return SITSTimeSeriesModel(instance=data)


@rpy2_fix_type
def sits_predictors(*args, **kwargs):
    """Obtain predictors for time series samples."""
    data = r_sits.sits_predictors(*args, **kwargs)

    return SITSPredictors(data)


#
# SOM
#
@rpy2_fix_type
def sits_som_map(*args, **kwargs):
    """Build a SOM for quality analysis of time series samples."""
    result = r_sits.sits_som_map(*args, **kwargs)

    return SITSOMData(result)
