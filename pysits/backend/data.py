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

"""backend module (based in R and sits)."""

from rpy2.robjects import r


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
