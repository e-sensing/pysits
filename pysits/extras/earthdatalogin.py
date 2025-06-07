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

"""Earthdatalogin module."""

from rpy2.robjects.packages import importr

from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc

#
# Package
#
r_pkg_earthdatalogin = importr("earthdatalogin")


#
# Functions
#
@function_call(r_pkg_earthdatalogin.edl_netrc, bool)
@attach_doc("earthdatalogin_edl_netrc")
def earthdatalogin_edl_netrc(*args, **kwargs) -> bool:
    """Set up Earthdata Login (EDL) credentials using a .netrc file."""
    ...


#
# List of functions to export
#
__all__ = ("earthdatalogin_edl_netrc",)
