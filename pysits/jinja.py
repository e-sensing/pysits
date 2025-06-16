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

"""Jinja2 template configuration."""

import os

from jinja2 import Environment, FileSystemLoader, Template

from pysits.sits.data import sits_bands, sits_bbox, sits_timeline


def get_template_env() -> Environment:
    """Get the Jinja2 template environment.

    Returns:
        Environment: Configured Jinja2 environment with sits functions in globals.
    """
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))

    # Add sits functions to globals
    # ToDo: Review functions to be added to the environment and define
    #       a more elegant way to do this.
    env.globals["sits_bands"] = sits_bands
    env.globals["sits_bbox"] = sits_bbox
    env.globals["sits_timeline"] = sits_timeline

    return env


def get_template(template_name: str) -> Template:
    """Get a template by name.

    Args:
        template_name: Name of the template file.

    Returns:
        Template: The requested template.
    """
    env = get_template_env()
    return env.get_template(template_name)
