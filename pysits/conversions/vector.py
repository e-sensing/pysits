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

"""Vector conversions."""

from pandas import DataFrame as PandasDataFrame
from rpy2.robjects.vectors import Vector

from pysits.backend.pkgs import r_pkg_base
from pysits.conversions.base import convert_to_python


def vector_to_pandas(vector: Vector) -> PandasDataFrame:
    """Convert a vector to a pandas dataframe."""
    # Get column names
    colnames = r_pkg_base.names(vector)
    colnames = convert_to_python(colnames, as_type="str")

    # Get values
    values = convert_to_python(vector, as_type="float")

    return PandasDataFrame({k: [v] for k, v in zip(colnames, values)})
