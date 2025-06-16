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

"""Configuration operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.base import SITStructureData


@function_call(r_pkg_sits.sits_config, SITStructureData)
@attach_doc("sits_config")
def sits_config(*args, **kwargs) -> SITStructureData:
    """Get/set sits configuration.

    ToDo:
        - Enhance result type to a Dict-like object.
    """


@function_call(r_pkg_sits.sits_config_show, lambda x: None)
@attach_doc("sits_config_show")
def sits_config_show(*args, **kwargs) -> None:
    """Show current sits configuration."""


@function_call(r_pkg_sits.sits_config_user_file, lambda x: None)
@attach_doc("sits_config_user_file")
def sits_config_user_file(*args, **kwargs) -> None:
    """Create a user configuration file."""
