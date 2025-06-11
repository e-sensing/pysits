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

"""Pytest configuration file."""

import webbrowser

import matplotlib

#
# Set the backend to avoid plot windows
#
matplotlib.use("Agg")

#
# Import after setting visualization backend
#
import matplotlib.pyplot as plt
import pytest


@pytest.fixture
def no_plot_window(monkeypatch):
    """Fixture to prevent matplotlib plot windows from showing during tests."""
    monkeypatch.setattr(plt, "show", lambda: None)
    yield
    plt.close("all")


@pytest.fixture
def no_browser(monkeypatch):
    """Fixture to prevent webbrowser from opening during tests."""
    monkeypatch.setattr(webbrowser, "open", lambda x: None)
    monkeypatch.setattr(webbrowser, "open_new", lambda x: None)
    monkeypatch.setattr(webbrowser, "open_new_tab", lambda x: None)
    yield
