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

"""Network operations."""

import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

import httpx2

#
# Supported URL schemes
#
REMOTE_SCHEMES = ("http", "https")


#
# Auxiliary functions
#
def is_remote(location: str | Path) -> bool:
    """Check if a location points to a remote resource.

    Args:
        location (str | Path): File location (local path or URL).

    Returns:
        bool: ``True`` when ``location`` is an URL with a supported scheme.

    Notes:
        - Supported schemes are ``http`` and ``https``.
    """
    return urlparse(str(location)).scheme in REMOTE_SCHEMES


#
# File management
#
@contextmanager
def fetch_to_tempfile(url: str, *, suffix: str = "") -> Iterator[Path]:
    """Download a remote file to a temporary file.

    Args:
        url (str): File URL.

        suffix (str): Suffix for the temporary file name.

    Yields:
        Path: Path of the downloaded file.

    Raises:
        httpx2.HTTPError: If the file cannot be downloaded.

    Notes:
        - The temporary file is removed when the context exits, including
        when the download fails or the caller raises.
    """
    # Create a temporary file
    descriptor, name = tempfile.mkstemp(suffix=suffix)

    # Name as path
    local_file = Path(name)

    # Try to download the file
    try:
        # Open the stream in binary mode
        with os.fdopen(descriptor, "wb") as stream:
            # Enable redirects to facilitate operations on remote files
            # stored in systems like huggingface and similar platforms.
            with httpx2.stream("GET", url, follow_redirects=True) as response:
                # Raise an exception if the response is not successful
                response.raise_for_status()

                # Write the content to the temporary file
                for chunk in response.iter_bytes():
                    stream.write(chunk)

        # Yield the path to the temporary file
        yield local_file

    finally:
        # Remove the temporary file
        local_file.unlink(missing_ok=True)
