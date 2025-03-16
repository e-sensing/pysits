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

"""factory utilities."""

from sitsflow.backend.sits import r_sits


def factory_function(name):
    """Factory to create sits-based functions.

    Args:
        name (str): name of the sits-based function.
    """
    if not hasattr(r_sits, name):
        raise ValueError(f"Invalid function: {name}")

    # define method closure
    def _fnc(*args, **kwargs):
        return getattr(r_sits, name)(*args, **kwargs)

    return _fnc
