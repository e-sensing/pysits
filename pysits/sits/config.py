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

from typing import Any

from pysits.backend.functions import r_fnc_sits_conf
from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.base import SITStructureData


def sits_config_value(*keys: str, default: Any = ...) -> Any:
    """Get a value from the sits configuration.

    Configuration values are addressed by the sequence of keys leading to them.
    As an example, the scale factor of a collection band is available at
    ``("sources", <source>, "collections", <collection>, "bands", <band>,
    "scale_factor")``.

    Args:
        *keys (str): Sequence of configuration keys.

        default (Any): Value returned when the keys are not available. When it
            is not defined, missing keys raise a ``KeyError``.

    Returns:
        Any: Configuration value. Values with a single element are returned as
            scalars.

    Raises:
        KeyError: When the keys are not available and no ``default`` is defined.

    Examples:
        >>> sits_config_value(
        ...     "sources", "BDC", "collections", "MOD13Q1-6.1",
        ...     "bands", "NDVI", "scale_factor"
        ... )
        0.0001
    """
    try:
        value = list(r_fnc_sits_conf(*keys))

    except Exception as e:
        if default is ...:
            raise KeyError(
                f"There is no sits configuration value for: {' -> '.join(keys)}"
            ) from e

        return default

    return value[0] if len(value) == 1 else value


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


@function_call(r_pkg_sits.sits_parallel, lambda x: None)
@attach_doc("sits_parallel")
def sits_parallel(*args, **kwargs) -> None:
    """Create sits cluster."""
