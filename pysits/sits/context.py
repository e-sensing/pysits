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

"""Global objects from sits."""

from pysits.sits.utils import load_samples_dataset

#
# Samples objects
#
cerrado_2classes = load_samples_dataset("cerrado_2classes", package="sits")

samples_modis_ndvi = load_samples_dataset("samples_modis_ndvi", package="sits")
samples_l8_rondonia_2bands = load_samples_dataset(
    "samples_l8_rondonia_2bands", package="sits"
)


#
# Points objects
#
point_mt_6bands = load_samples_dataset("point_mt_6bands", package="sits")
