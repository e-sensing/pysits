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

"""classification example."""

import os

from pysits import *

#
# General definitions
#
output_dir = "data/output/copy"


#
# 1. Create directory
#
os.makedirs(output_dir, exist_ok=True)


#
# 2. Define cube
#
bdc_cube = sits_cube(
    source="BDC",
    collection="CBERS-WFI-16D",
    tiles=["007004", "007005"],
    bands=["B15", "CLOUD"],
    start_date="2018-01-01",
    end_date="2018-01-12",
)


#
# 3. Copy from remote to local
#
cube_local = sits_cube_copy(
    cube=bdc_cube,
    output_dir=output_dir,
    roi=dict(lon_min=-46.5, lat_min=-45.5, lon_max=-15.5, lat_max=-14.6),
    multicores=2,
    res=250,
)
