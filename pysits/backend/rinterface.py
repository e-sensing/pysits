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

"""R interface used by ``pysits``."""

import logging

#
# Logger `rpy2` uses to report the API to ABI fallback
#
RPY2_OPENRLIB_LOGGER = "rpy2.rinterface_lib.openrlib"

#
# Get logger from rpy2
#
_logger = logging.getLogger(RPY2_OPENRLIB_LOGGER)

# Set on import: the notice is emitted when `rpy2` is first imported
# If a level is already set on the logger, we do not change it. This
# allows users to opt back in with:
# logging.getLogger(RPY2_OPENRLIB_LOGGER).setLevel(logging.DEBUG)
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.ERROR)


def r_interface_mode() -> str:
    """Report the ``cffi`` mode ``rpy2`` is using to reach R.

    Returns:
        str: ``"API"`` when `rpy2` loaded its compiled extension, `"ABI"`
                when it resolves R symbols at run time.
    """
    from rpy2.rinterface_lib.openrlib import cffi_mode

    return cffi_mode.value
