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

"""Utilities operations."""

from pathlib import Path

from pysits.backend.functions import r_fnc_read_rds, r_fnc_set_seed, r_fnc_system_file
from pysits.backend.loaders import load_data_from_global, load_data_from_package
from pysits.models.data.frame import SITSFrame
from pysits.models.data.ts import SITSTimeSeriesModel
from pysits.models.resolver import (
    resolve_and_invoke_accuracy_class,
    resolve_and_invoke_content_class,
)

#
# Data class resolver
#
RDS_RESOLVERS = [
    resolve_and_invoke_content_class,
    resolve_and_invoke_accuracy_class,
]


#
# State management
#
def r_set_seed(seed: int) -> None:
    """Set seed for random number generation.

    Args:
        seed (int): Seed value.
    """
    r_fnc_set_seed(seed)


#
# File management
#
def read_rds(file: str | Path) -> SITSFrame:
    """Read RDS file compatible with SITS.

    Args:
        file (str | Path): RDS file.

    Returns:
        SITSFrame: SITS Data instance (can be a ``cube`` or a ``time-series`` object).
    """
    file = Path(file)

    # Check if file exists
    if not file.exists():
        raise FileNotFoundError("Failed to read RDS: File does not exist.")

    # Read RDS
    rds_content = r_fnc_read_rds(file.as_posix())

    # Resolve and invoke data class
    for resolver in RDS_RESOLVERS:
        try:
            return resolver(rds_content)

        except ValueError:
            continue

    # Raise an error if no class was selected
    raise ValueError(
        "Unknown or unsupported R object: Only sits-related objects are supported."
    )


def r_package_dir(content_dir: str, package: str) -> Path | None:
    """Get data dir from an existing R package.

    This function gets the directory available in an R package. It uses
    `system.file` behind the scenes.

    Args:
        content_dir (str): Directory in the package.

        package (str): R Package name.

    Returns:
        Path | None: If available, returns ``pathlib.Path``. Otherwise, returns None.
    """
    dir_path = r_fnc_system_file(content_dir, package=package)
    dir_path = dir_path[0]  # required as rpy2 returns a list

    dir_path = Path(dir_path)

    return None if not dir_path.exists() else dir_path


def load_samples_dataset(name: str, package: str, **kwargs) -> SITSTimeSeriesModel:
    """Load sits data from package.

    Args:
        name (str): Dataset name.

        package (str): Package name.

        **kwargs: Additional arguments to pass to the function.
    """
    # Load data from package
    load_data_from_package(name, package, **kwargs)

    # Load data from global environment
    data = load_data_from_global(name)

    # Return data
    return SITSTimeSeriesModel(data)
