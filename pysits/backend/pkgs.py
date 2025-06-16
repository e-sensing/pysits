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

"""backend packages."""

from rpy2.robjects.packages import importr

# system pakage
r_pkg_base = importr("base")
r_pkg_grdevices = importr("grDevices")

# sits package
r_pkg_sits = importr("sits")

# sits-dependencies packages
r_pkg_tibble = importr("tibble")
r_pkg_leaflet = importr("leaflet")
r_pkg_kohonen = importr("kohonen")
r_pkg_sf = importr("sf")
r_pkg_htmlwidgets = importr("htmlwidgets")
r_pkg_arrow = importr("arrow")
