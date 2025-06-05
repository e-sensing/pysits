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

"""Unit tests for data operations (cube and time-series)."""

import pytest


def test_lazy_import():
    """Test lazy import of extras."""
    from pysits.extras import earthdatalogin_edl_netrc

    assert earthdatalogin_edl_netrc is not None


def test_lazy_import_error():
    """Test lazy import of extras."""

    with pytest.raises(ImportError):
        from pysits.extras import invalidmodule_function_name  # noqa: F401


def test_earthdatalogin():
    """Test earthdatalogin functions."""
    from pysits.extras import earthdatalogin_edl_netrc

    assert earthdatalogin_edl_netrc(username="test", password="test")


def test_torch():
    """Test torch functions."""
    from pysits.extras import torch_install_torch

    assert torch_install_torch()
