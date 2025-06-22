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

"""Settings module."""

import os
import warnings

import rpy2.rinterface_lib.callbacks

#
# Warning/print management
#
# Suppress rpy2 warnings
warnings.filterwarnings("ignore", module=r"rpy2.*")

# Suppress R warnings and errors
rpy2.rinterface_lib.callbacks.consolewrite_warnerror = lambda x: None

#
# Environment variables
#
os.environ["TORCH_INSTALL"] = "0"

#
# Package version
#
__version__ = "1.5.3.dev1"

__all__ = ("__version__",)
