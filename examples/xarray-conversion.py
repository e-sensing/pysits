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

"""xarray exporter example."""

from pysits import *

#
# General definition
#

# Cube directory
cube_dir = "data/cube/"

# Samples file
samples_file = "data/samples/samples_sinop_crop.csv"


#
# 1. Load cube
#
cube = sits_cube(
    source="BDC",
    collection="MOD13Q1-6.1",
    data_dir=cube_dir,
)

#
# 2. Get time series
#
samples_ts = sits_get_data(
    cube=cube,
    samples=samples_file,
)


#
# 3. Time series as xarray
#
xsamples_ts = sits_as_xarray(samples_ts)

xsamples_ts

#
# 4. Cube as xarray
#
xcube = sits_as_xarray(cube)

xcube
