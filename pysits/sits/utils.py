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

"""utilities operations."""

from pathlib import Path

from pysits.backend.utils import r_class, r_read_rds
from pysits.models import SITSCubeModel, SITSData, SITSTimeSeriesModel


def read_sits_rds(file: str | Path) -> SITSData:
    """Read sits data stored as RDS file.

    Args:
        file (str | Path): RDS file.

    Returns:
        SITSData: SITS Data instance (can be a ``cube`` or a ``time-series`` object).
    """
    file = Path(file)

    # Check if file exists
    if not file.exists():
        raise FileNotFoundError("Failed to read RDS: File does not exist.")

    # Read RDS
    rds_content = r_read_rds(file.as_posix())

    # Get content class
    rds_class = r_class(rds_content)

    # Check class
    content_class = None

    match rds_class:
        # Time-series data (``sits``)
        case class_ if "sits" in class_:
            content_class = SITSTimeSeriesModel

        # Data Cube (``raster_cube``)
        case class_ if "raster_cube" in class_:
            content_class = SITSCubeModel

    # Raise an error if no class was selected
    if not content_class:
        raise ValueError(
            "Unknown or unsupported R object: Only sits objects are supported."
        )

    return content_class(rds_content)
