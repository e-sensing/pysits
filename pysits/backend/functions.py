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

"""backend utility functions."""

from pysits.backend.pkgs import r_pkg_base

#
# Base - Plot
#
r_fnc_plot = r_pkg_base.plot

#
# Base - summary
#
r_fnc_summary = r_pkg_base.summary

#
# Base - readRDS
#
r_fnc_read_rds = r_pkg_base.readRDS

#
# Base - system.file
#
r_fnc_system_file = r_pkg_base.system_file

#
# Base - set.seed
#
r_fnc_set_seed = r_pkg_base.set_seed

#
# Base - Class
#
r_fnc_class = getattr(r_pkg_base, "class")
