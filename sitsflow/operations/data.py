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

"""data management operations."""

from sitsflow.backend.sits import r_sits
from sitsflow.types import r_to_python, rpy2_fix_type


@rpy2_fix_type
def sits_bands(*args, **kwargs):
    """Get datacube bands.

    Finds the names of the bands of a set of time series or of a data cube.
    """
    data = r_sits.sits_bands(*args, **kwargs)
    return r_to_python(data, as_type="str")


@rpy2_fix_type
def sits_timeline(*args, **kwargs):
    """Get datacube timeline.

    This function returns the timeline for a given data set, either a set of
    time series, a data cube, or a trained model.
    """
    data = r_sits.sits_timeline(*args, **kwargs)
    return r_to_python(data, as_type="date")


@rpy2_fix_type
def sits_labels(*args, **kwargs):
    """Finds labels in a sits tibble or data cube."""
    data = r_sits.sits_labels(*args, **kwargs)

    return r_to_python(data, as_type="str")


@rpy2_fix_type
def sits_list_collections(*args, **kwargs):
    """List collections available.

    Prints the collections available in each cloud
    service supported by sits. Users can select to get
    information only for a single service by using the
    source parameter.
    """
    r_sits.sits_list_collections(*args, **kwargs)
