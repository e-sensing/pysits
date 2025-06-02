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

from pysits.backend.data import load_global_data
from pysits.models.ts import SITSTimeSeriesModel


#
# Auxiliary function
#
def _load_samples_dataset(name: str) -> SITSTimeSeriesModel:
    """Load samples dataset from r environment.

    Args:
        name (str): Dataset name.

    Returns:
        SITSTimeSeriesModel: Dataset model.
    """
    return SITSTimeSeriesModel(load_global_data(name))


#
# Samples objects
#
cerrado_2classes = _load_samples_dataset("cerrado_2classes")

samples_modis_ndvi = _load_samples_dataset("samples_modis_ndvi")
samples_l8_rondonia_2bands = _load_samples_dataset("samples_l8_rondonia_2bands")


#
# Points objects
#
point_mt_6bands = _load_samples_dataset("point_mt_6bands")
