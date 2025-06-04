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

"""Extras module for pysits."""

import importlib
import sys
from collections.abc import Callable

#
# List of extras modules
#
EXTRAS_MODULES: list[str] = [
    "earthdatalogin",
    "torch",
]


#
# Lazy loading mechanism
#
def __getattr__(name: str) -> Callable:
    """Lazily import and return a function from a submodule.

    This function implements the lazy loading mechanism. It uses the function name
    prefix to determine which module to import from. Functions must follow the
    pattern: <modulename>_<function name>.

    Args:
        name: The name of the function to import. Must start with a valid module
              name from ``EXTRAS_MODULES``.

    Returns:
        Callable: The requested function from the appropriate submodule.

    Raises:
        AttributeError: If the function doesn't exist or if the module prefix
                        is not recognized.

        ImportError: If there are issues importing the required module.

    Example:
        >>> # This will trigger __getattr__("earthdatalogin_edl_netrc")
        >>> from pysits.extras import earthdatalogin_edl_netrc
    """
    # Get the current module
    current_module = sys.modules[__name__]

    # Find the module name from the function prefix
    for module_name in EXTRAS_MODULES:
        if name.startswith(f"{module_name}_"):
            try:
                # Import module
                module = importlib.import_module(f".{module_name}", package=__name__)

                # Check if the attribute exists in the module
                if hasattr(module, name):
                    # Get the attribute
                    attr = getattr(module, name)

                    # Cache it in the current module for future access
                    setattr(current_module, name, attr)

                    return attr
            except ImportError:
                break

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
