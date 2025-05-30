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

"""regularization example."""

import os

from pysits import *

#
# General definition
#

# Output directory
output_dir = "data/output/regularization"


#
# 1. Create directory
#
os.makedirs(output_dir, exist_ok=True)


#
# 2. Load cube
#
cube = sits_cube(
    source="AWS",
    collection="SENTINEL-2-L2A",
    tiles=("20LKP", "20LLP"),
    bands=("B8A", "CLOUD"),
    start_date="2018-10-01",
    end_date="2018-11-01",
)

#
# 3. Get cube bands
#
sits_bands(cube)


#
# 4. Get cube timeline
#
sits_timeline(cube)


#
# 5. Regularize
#
cube_reg = sits_regularize(
    cube=cube,
    period="P16D",
    res=10,
    multicores=12,
    output_dir=output_dir,
)


#
# 6. Plot
#
plot(cube_reg, band="B8A")
