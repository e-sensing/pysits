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

"""Torch module."""

from rpy2.robjects.packages import importr

from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc

#
# Package
#
r_pkg_torch = importr("torch", on_conflict="warn")


#
# Functions
#
@function_call(r_pkg_torch.install_torch, bool)
@attach_doc("torch_install_torch")
def torch_install_torch(*args, **kwargs) -> bool:
    """Install Torch."""
    ...


#
# List of functions to export
#
__all__ = ("torch_install_torch",)
