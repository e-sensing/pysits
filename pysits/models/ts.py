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

"""time-series models."""

from pysits.backend.utils import r_plot
from pysits.models.base import SITSModel


#
# Base class
#
class SITSTimeSeriesModel(SITSModel):
    """Time-series base class."""

    def _plot(self, *args, **kwargs):
        """Plot time-series data."""
        return r_plot(self._instance, *args, **kwargs)
