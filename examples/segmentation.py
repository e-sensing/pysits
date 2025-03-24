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

"""segmentation example."""

import os

from pysits import *

#
# General definition
#
# Output directory
output_dir = "data/output/segmentation"

# Cube directory
cube_dir = "data/cube/"

# Samples file
samples_file = "data/samples/samples_sinop_crop.csv"


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
# 3. Get cube bands
#
sits_bands(cube)


#
# 4. Get cube timeline
#
sits_timeline(cube)


#
# 5. Segment cube
#
segments = sits_segment(
    cube=cube,
    seg_fn=sits_slic(),
    output_dir=output_dir,
)


#
# 6. Get time series
#
samples_ts = sits_get_data(
    cube=cube,
    samples=samples_file,
)


#
# 7. Train model
#
rfor_model = sits_train(
    samples=samples_ts,
    ml_method=sits_rfor(),
)


#
# 8. Classify segments
#
probs_cube = sits_classify(
    data=segments,
    ml_model=rfor_model,
    output_dir=output_dir,
)


#
# 9. Label classification
#
label_cube = sits_label_classification(
    cube=probs_cube,
    output_dir=output_dir,
)


#
# 10. Plot
#
plot(label_cube)
