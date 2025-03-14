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

"""cube models."""

from sitsflow.models.base import SITSModel
from sitsflow.plot.tmap import plot_tmap


#
# Base class
#
class SITSCubeModel(SITSModel):
    """Base class for sitsflow cubes."""

    def _plot(self, *args, **kwargs):
        """Plot cube using tmap."""
        plot_tmap(self._instance, *args, **kwargs)
