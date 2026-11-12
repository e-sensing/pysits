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

"""Unit tests for network operations."""

import socket
import tempfile
from pathlib import Path
from threading import Thread

import httpx2
import pytest

from pysits.network import fetch_to_tempfile, is_remote


#
# Auxiliary functions
#
def temporary_files() -> set[Path]:
    """List the files currently in the temporary directory."""
    return set(Path(tempfile.gettempdir()).iterdir())


#
# Fixtures
#
@pytest.fixture
def raw_server():
    """HTTP Server."""
    server_sockets = []

    def start(response: bytes) -> str:
        """Start the HTTP server."""
        # Create a socket and bind it to a random port
        server_socket = socket.socket()
        server_socket.bind(("127.0.0.1", 0))
        server_socket.listen(1)
        server_sockets.append(server_socket)

        # Start a thread to serve the response
        def serve() -> None:
            try:
                connection, _ = server_socket.accept()
                connection.recv(4096)
                connection.sendall(response)
                connection.close()

            except OSError:
                pass

        # Start the thread
        Thread(target=serve, daemon=True).start()

        # Return the URL of the server
        return f"http://127.0.0.1:{server_socket.getsockname()[1]}/samples.rds"

    yield start

    for server_socket in server_sockets:
        server_socket.close()


#
# Tests
#
@pytest.mark.parametrize(
    ("location", "expected"),
    [
        ("https://example.org/samples.rds", True),
        ("http://example.org/samples.rds", True),
        ("/data/samples.rds", False),
        ("/home/user/samples.rds", False),
        # Note: ``urlparse`` reads the drive letter as the scheme,
        # so a Windows path must not be mistaken for a remote location
        (r"C:\data\samples.rds", False),
    ],
)
def test_is_remote(location: str, expected: bool):
    """Test remote location identification."""
    assert is_remote(location) is expected


def test_fetch_to_tempfile_downloads_and_cleans_up(http_server):
    """Test remote content download."""
    directory, base_url = http_server

    # Save payload
    samples_file_local = directory / "samples.rds"
    samples_file_local.write_bytes(b"sits-payload")

    # Fetch the file
    samples_file_remote = f"{base_url}/samples.rds"

    with fetch_to_tempfile(samples_file_remote, suffix=".rds") as local_file:
        assert local_file.read_bytes() == b"sits-payload"

    # Check the file is deleted
    assert not local_file.exists()


def test_fetch_to_tempfile_follows_redirects(http_server):
    """Test redirect following."""
    directory, base_url = http_server

    # Save payload
    samples_file_local = directory / "samples.rds"
    samples_file_local.write_bytes(b"sits-payload")

    # Fetch the file
    samples_file_remote = f"{base_url}/redirect/samples.rds"

    with fetch_to_tempfile(samples_file_remote, suffix=".rds") as local_file:
        assert local_file.read_bytes() == b"sits-payload"


def test_fetch_to_tempfile_rejects_error_status(http_server):
    """Test error response handling."""
    _, base_url = http_server

    # Save payload
    before = temporary_files()

    # Fetch file
    with pytest.raises(httpx2.HTTPStatusError):
        with fetch_to_tempfile(f"{base_url}/non-existing-file.rds"):
            pass

    assert temporary_files() == before


def test_fetch_to_tempfile_rejects_truncated_response(raw_server):
    """Test truncated response handling."""
    # Create a server that returns a truncated response
    url = raw_server(b"HTTP/1.1 200 OK\r\nContent-Length: 5000\r\n\r\n" + b"x" * 100)

    # Save payload
    before = temporary_files()

    # Fetch file
    with pytest.raises(httpx2.RemoteProtocolError):
        with fetch_to_tempfile(url):
            pass

    # Check the file is deleted
    assert temporary_files() == before
