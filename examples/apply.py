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

"""apply example."""

import os

from pysits import *

#
# General definition
#
# Output directory
output_dir = "data/output/apply"

# Cube directory
cube_dir = "data/cube/"


#
# 1. Create directory
#
os.makedirs(output_dir, exist_ok=True)


#
# 2. Load cube
#
cube = sits_cube(
    source="BDC",
    collection="MOD13Q1-6.1",
    data_dir=cube_dir,
)


#
# 3. Apply
#

# NDVI Median
cube_apply = sits_apply(
    data=cube,
    NDVIMEDIAN="w_median(NDVI)",
    window_size=5,
    output_dir=output_dir,
    multicores=4,
)

# NDVI / 2
cube_apply = sits_apply(
    data=cube_apply,
    NDVIDIV="NDVI / 2",
    window_size=5,
    output_dir=output_dir,
    multicores=4,
)

#
# 4. Plot
#

# NDVI Median
plot(cube_apply, band="NDVIMEDIAN")

# NDVI / 2
plot(cube_apply, band="NDVIDIV")
