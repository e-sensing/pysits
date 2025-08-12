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

from pysits.backend.loaders import load_package
from pysits.settings import __sitsver__

# system pakage
r_pkg_base = load_package("base")
r_pkg_grdevices = load_package("grDevices")

# sits package
r_pkg_sits = load_package("sits", min_version=__sitsver__)

# sits-dependencies packages
r_pkg_tibble = load_package("tibble")
r_pkg_leaflet = load_package("leaflet")
r_pkg_kohonen = load_package("kohonen")
r_pkg_sf = load_package("sf")
r_pkg_htmlwidgets = load_package("htmlwidgets")
r_pkg_arrow = load_package("arrow")
