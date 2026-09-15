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

import os

# Some tests drive `pyplot` to check how figures are handed to a host.
# Pinning the backend before matplotlib is imported keeps that from
# selecting a windowing backend on a machine without a display.
os.environ.setdefault("MPLBACKEND", "Agg")

import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any

import matplotlib
import pytest
import rpy2.robjects as ro

from pysits.models.data.cube import SITSCubeModel
from pysits.sits.cube import sits_cube
from pysits.sits.utils import r_package_dir
from pysits.visualization.options import reset_plot_options

#
# Path prefix the test server answers with a redirect
#
REDIRECT_PREFIX = "/redirect/"


#
# Helpers
#
def r_closure_value(method: Any, name: str) -> Any:
    """Read a value stored in the R closure of a ml/dl method."""
    return ro.r["environment"](method)[name]


def r_opt_hparams(method: Any) -> dict[str, float]:
    """Read the optimizer hyperparameters of a ml/dl method."""
    hparams = r_closure_value(method, "opt_hparams")

    return {k: v[0] for k, v in zip(hparams.names, hparams, strict=True)}


def r_class(obj: Any) -> list[str]:
    """Read the classes of an R object."""
    return list(ro.r["class"](obj))


def r_identical(x: Any, y: Any) -> bool:
    """Check if two R objects are identical."""
    return bool(ro.r["identical"](x, y)[0])


def r_open_devices() -> int:
    """Count the R graphics devices currently open."""
    devices = ro.r["dev.list"]()

    return 0 if devices == ro.NULL else len(devices)


#
# Fixtures
#
@pytest.fixture(scope="module")
def local_cube() -> SITSCubeModel:
    """Cube created from local files."""
    return sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=r_package_dir("extdata/raster/mod13q1", package="sits"),
        progress=False,
    )


@pytest.fixture(autouse=True)
def clean_plot_state():
    """Fixture to keep plot state from leaking between tests.

    Figures are rendered on R graphics devices, which live in the R session
    and would otherwise outlive the test that opened them. The rendering
    geometry is process-wide for the same reason.
    """
    yield

    reset_plot_options()
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)

    assert r_open_devices() == 0, "test left an R graphics device open"


@pytest.fixture
def no_browser(monkeypatch):
    """Fixture to prevent webbrowser from opening during tests."""
    monkeypatch.setattr(webbrowser, "open", lambda x: None)
    monkeypatch.setattr(webbrowser, "open_new", lambda x: None)
    monkeypatch.setattr(webbrowser, "open_new_tab", lambda x: None)

    yield


class _RedirectingRequestHandler(SimpleHTTPRequestHandler):
    """Serve a directory with a redirect."""

    def do_GET(self) -> None:  # noqa: N802 (name defined by the base class)
        # If path starts with a given prefix, simulate a redirect
        if self.path.startswith(REDIRECT_PREFIX):
            # Simulate a redirect
            self.send_response(302)
            self.send_header("Location", self.path[len(REDIRECT_PREFIX) - 1 :])
            self.end_headers()

            return

        super().do_GET()

    def log_message(self, *args, **kwargs) -> None:
        """Keep the per-request log out of the test output."""


@pytest.fixture
def http_server(tmp_path: Path):
    """HTTP server serving a directory with a redirect."""
    handler = partial(
        _RedirectingRequestHandler,
        directory=str(tmp_path),
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)

    # Start the server in a daemon thread
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Yield the directory and its base URL
    try:
        yield tmp_path, f"http://127.0.0.1:{server.server_port}"

    # Shutdown the server
    finally:
        server.shutdown()
        server.server_close()
