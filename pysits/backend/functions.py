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

"""backend functions."""

from pysits.backend.loaders import load_function_from_package

# Base - plot
r_fnc_plot = load_function_from_package("base::plot")

# Base - summary (base)
r_fnc_summary = load_function_from_package("base::summary")

# Base - readRDS (base)
r_fnc_read_rds = load_function_from_package("base::readRDS")

# Base - system.file (base)
r_fnc_system_file = load_function_from_package("base::system_file")

# Base - set.seed (base)
r_fnc_set_seed = load_function_from_package("base::set_seed")

# Base - class (base)
r_fnc_class = load_function_from_package("base::class")
