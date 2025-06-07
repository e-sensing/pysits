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

"""backend loaders."""

from collections.abc import Callable
from typing import Any

from rpy2.robjects import r
from rpy2.robjects.packages import importr


def load_data_from_package(name: str, package: str, **kwargs) -> object:
    """Load data from package.

    This function loads data from a package. It uses `data` behind the scenes.

    Args:
        name (str): Dataset name.

        package (str): Package name.

        **kwargs: Additional arguments to pass to the function.
    """
    return r.data(name, package=package, **kwargs)


def load_data_from_global(name: str) -> object:
    """Load data from global environment.

    This function loads data from the global environment.

    Args:
        name (str): Dataset name.
    """
    return r[name]


def load_function_from_package(name: str) -> Callable[..., Any]:
    """Load an R function from a specified package.

    This function takes a fully qualified R function name in the format
    'package::function' and returns a callable Python wrapper for that R function.

    Args:
        name (str): The fully qualified name of the R  function in the format
                    'package::function'. For example, 'stats::median' or 'base::mean'.

    Returns:
        Callable[..., Any]: A Python callable that wraps the R function.
                            The exact signature depends on the underlying R function.

    Raises:
        ValueError: If the ``name`` doesn't follow the 'package::function' format.

        PackageNotFoundError: If the specified R package is not installed.

        AttributeError: If the function doesn't exist in the specified package.

    Examples:
        >>> median_func = load_function_from_package('stats::median')
        >>> result = median_func([1, 2, 3, 4, 5])
    """
    # Parse package and function
    try:
        package_name, func_name = name.split("::")

    except ValueError as e:
        raise ValueError(
            f"Invalid function name format: {name}. "
            "Expected format: 'package::function'"
        ) from e

    # Import the package
    pkg = importr(package_name, on_conflict="warn")

    # Return function
    return getattr(pkg, func_name)
