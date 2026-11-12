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

"""Tests for the R interface backend."""

import subprocess
import sys

from pysits import r_interface_mode


def test_import_pysits_reports_no_cffi_fallback():
    """Importing `pysits` must not print `rpy2` API/ABI fallback notices."""
    proc = subprocess.run(
        [sys.executable, "-c", "import pysits"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr
    assert "Error importing in API mode" not in proc.stderr
    assert "Trying to import in ABI mode" not in proc.stderr


def test_r_interface_mode_reports_a_supported_mode():
    """interface mode must return a valid value."""
    assert r_interface_mode() in {"API", "ABI"}
