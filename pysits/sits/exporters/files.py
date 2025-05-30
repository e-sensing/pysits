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

"""Files exporter."""

from pandas import DataFrame as PandasDataFrame

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.base import rpy2_fix_type
from pysits.models import SITSData


@rpy2_fix_type
def sits_as_csv(*args, **kwargs) -> PandasDataFrame:
    """Export sits data as csv."""
    data = r_pkg_sits.sits_to_csv(*args, **kwargs)

    return SITSData(data)
