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

"""Arrow interoperability between R and Python.

``pysits`` moves data between R and Python as Arrow IPC streams. That puts two
independent builds of the libarrow C++ library in a single process: the one
bundled in the R ``arrow`` package and the one bundled in ``pyarrow``. Their
symbols collapse into a single namespace, so a call made through ``pyarrow``
can be served by R's libarrow.

Each build keeps a private ``mimalloc`` heap. When the two are mixed, a buffer
allocated by one library is read back as zeroed memory by the other, and every
transfer is silently corrupted instead of failing. Both builds also support the
system allocator, which is shared, so selecting it keeps them interoperable.

The allocator is chosen by libarrow the first time it initializes, so importing
this module sets ``ARROW_DEFAULT_MEMORY_POOL``. It is imported before anything
that pulls in ``pyarrow`` or the R ``arrow`` package.
"""

import os

#
# Allocator selected to keep R libarrow and pyarrow interoperable
#
ARROW_MEMORY_POOL_ENVVAR = "ARROW_DEFAULT_MEMORY_POOL"
ARROW_MEMORY_POOL = "system"

# Set on import: libarrow reads this once, when it initializes. A value already
# present in the environment is left alone so users can override it.
os.environ.setdefault(ARROW_MEMORY_POOL_ENVVAR, ARROW_MEMORY_POOL)

#
# Values transferred to R and back to verify the round-trip is lossless. A
# mismatched pair of libarrow builds reads them back as zeros.
#
PROBE_COLUMN = "pysits_arrow_probe"
PROBE_VALUES = [0.5, 1.5, 2.5]


def check_arrow_memory_pool() -> None:
    """Refuse to load R ``arrow`` package under an unshared allocator.

    Called before the R ``arrow`` package is loaded. Corruption appears only
    once both libarrow builds are in use, and is silent when it does, so the
    configuration is rejected up front rather than probed for afterwards.

    Raises:
        RuntimeError: If the selected allocator is not the shared one.
    """
    selected = os.environ.get(ARROW_MEMORY_POOL_ENVVAR)

    if selected == ARROW_MEMORY_POOL:
        return

    raise RuntimeError(
        f"{ARROW_MEMORY_POOL_ENVVAR} is set to '{selected}', but pysits "
        f"requires '{ARROW_MEMORY_POOL}'.\n\n"
        "The R `arrow` package and `pyarrow` each bundle their own build of "
        "the libarrow C++ library. Loaded together, they must use the system "
        "allocator to share buffers. With any other allocator, data sent "
        "between R and Python is silently replaced by zeros.\n\n"
        f"Unset {ARROW_MEMORY_POOL_ENVVAR}, or set it before starting Python:\n\n"
        f"    export {ARROW_MEMORY_POOL_ENVVAR}={ARROW_MEMORY_POOL}"
    )


def arrow_interop_error(observed: list) -> RuntimeError:
    """Build the error raised when an Arrow round-trip loses data.

    Args:
        observed (list): Values read back from R for `PROBE_VALUES`.

    Returns:
        RuntimeError: Error describing the cause and how to resolve it.
    """
    import pyarrow as pa

    pool = pa.default_memory_pool().backend_name

    return RuntimeError(
        "Data sent to R is coming back corrupted, so pysits cannot run.\n\n"
        f"Sent {PROBE_VALUES}, received {observed}.\n\n"
        "The R `arrow` package and `pyarrow` each bundle their own build of "
        "the libarrow C++ library. Loaded together, they must use the system "
        f"allocator to share buffers, but pyarrow is using '{pool}'.\n\n"
        "This happens when pyarrow is initialized before pysits with a "
        "different allocator. Either import pysits before pyarrow, or set the "
        "environment variable before starting Python:\n\n"
        f"    export {ARROW_MEMORY_POOL_ENVVAR}={ARROW_MEMORY_POOL}"
    )
