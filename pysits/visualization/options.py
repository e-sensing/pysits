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

"""Plot rendering options."""

import math

import matplotlib
import rpy2.robjects as ro

from pysits.models.visual import ImageArgs, PlotOptions

#
# Constants
#
IMAGE_ARGS_KEYS = {
    "width": "width",
    "height": "height",
    "res": "dpi",
    "dpi": "dpi",
}
"""Mapping between ``image_args`` keys and ``PlotOptions`` fields."""

KNITR_OPTION_KEYS = {
    "fig.width": "width",
    "fig.height": "height",
    "dpi": "dpi",
}
"""Mapping between ``knitr`` chunk options and ``PlotOptions`` fields."""

KNITR_OPTIONS_QUERY = """
local({
  keys <- c("fig.width", "fig.height", "dpi")

  if (!isTRUE(getOption("knitr.in.progress")) ||
      !requireNamespace("knitr", quietly = TRUE)) {
    return(rep(NA_real_, length(keys)))
  }

  options <- knitr::opts_current$get()

  vapply(
    keys,
    function(key) {
      value <- options[[key]]
      if (is.null(value)) NA_real_ else as.numeric(value)[1]
    },
    numeric(1)
  )
})
"""
"""R expression reading the geometry of the chunk being rendered.

Returns one value per key of `KNITR_OPTION_KEYS`, in order, with
`NA` standing for an option the chunk does not set.
"""


#
# Module state
#
_overrides = {}
"""Geometry set explicitly through `set_plot_options`."""


#
# Utility functions
#
def _from_image_args(image_args: ImageArgs | None) -> dict[str, float]:
    """Translate `image_args` into `PlotOptions` fields.

    Args:
        image_args (dict): Per-call image configuration.

    Returns:
        dict: The corresponding `PlotOptions` fields.

    Raises:
        ValueError: If `image_args` contains an unknown key.
    """
    if not image_args:
        return {}

    # Check for unknown keys
    unknown = set(image_args) - set(IMAGE_ARGS_KEYS)

    # Raise if any are found
    if unknown:
        raise ValueError(
            f"Unknown image_args: {', '.join(sorted(unknown))}. "
            f"Supported keys: {', '.join(sorted(IMAGE_ARGS_KEYS))}."
        )

    # Translate keys to fields and return!
    return {
        IMAGE_ARGS_KEYS[key]: value
        for key, value in image_args.items()
        if key in IMAGE_ARGS_KEYS
    }


def _from_host() -> dict[str, float]:
    """Read the figure geometry configured by the host environment.

    ``matplotlib.rcParams`` is the channel documents use to declare their
    figure geometry to Python. Quarto, for example, writes the document-level
    `fig-width`, `fig-height`, and `fig-dpi` options straight into it
    when it starts the kernel.

    Only values that differ from the matplotlib factory defaults are
    reported, so an unconfigured session falls back to the pysits defaults
    rather than to matplotlib much smaller ones.

    Returns:
        dict: The `PlotOptions` fields configured by the host, if any.
    """
    values = {}

    # Get current figure size
    figsize = tuple(matplotlib.rcParams["figure.figsize"])

    # If different from default, add to values
    if figsize != tuple(matplotlib.rcParamsDefault["figure.figsize"]):
        values["width"], values["height"] = figsize

    # Get current DPI
    dpi = matplotlib.rcParams["figure.dpi"]

    # If different from default, add to values
    if dpi != matplotlib.rcParamsDefault["figure.dpi"]:
        values["dpi"] = round(dpi)

    # Return!
    return values


def _from_knitr() -> dict[str, float]:
    """Read the figure geometry of the `knitr` chunk being rendered.

    ``knitr`` keeps the geometry of the chunk it is rendering in its own
    options rather than in `matplotlib.rcParams`, and its `dpi` already
    accounts for the document setting. Reading it lets R draw at exactly the
    size the document writes the figure at, with no resampling between.

    This works because `reticulate` runs Python inside the same R session
    `knitr` is rendering from, so `rpy2` reaches the same options.

    Outside that setup the query reports nothing, and any failure to reach
    R at all is ignored.

    Returns:
        dict: The ``PlotOptions`` fields declared by the chunk, if any.
    """
    try:
        # Get knitr options
        values = list(ro.r(KNITR_OPTIONS_QUERY))

    except Exception:
        return {}

    # Filter out NAs and convert to fields
    declared = {
        field: value
        for field, value in zip(KNITR_OPTION_KEYS.values(), values, strict=True)
        if value is not None and not math.isnan(value)
    }

    # Round DPI to nearest integer
    if "dpi" in declared:
        declared["dpi"] = round(declared["dpi"])

    # Return!
    return declared


#
# High-level operations
#
def resolve_plot_options(image_args: ImageArgs | None = None) -> PlotOptions:
    """Resolve plot options.

    Plot options are resolved in order, each overriding the previous one:

    1. the pysits defaults;
    2. the host environment;
    3. the `knitr` chunk being rendered;
    4. values set through `set_plot_options`;
    5. the per-call `image_args`.

    Args:
        image_args (dict): Per-call image configuration, with any of the
                           keys `width` and `height` (in inches), and
                           `res` (in dots per inch).

    Returns:
        PlotOptions: The geometry to render with.
    """
    return PlotOptions(
        **{
            **_from_host(),
            **_from_knitr(),
            **_overrides,
            **_from_image_args(image_args),
        }
    )


def get_plot_options() -> PlotOptions:
    """Get the plot options in effect.

    Returns:
        PlotOptions: The plot options in effect.
    """
    return resolve_plot_options()


def set_plot_options(
    width: float | None = None,
    height: float | None = None,
    dpi: int | None = None,
) -> PlotOptions:
    """Set plot options.

    Plot options set here apply to every subsequent plot, and take precedence
    over the options declared by the host document. Arguments left as
    `None` are not changed.

    Args:
        width (float): Plot width, in inches.

        height (float): Figure height, in inches.

        dpi (int): Rendering resolution, in dots per inch.

    Returns:
        PlotOptions: The geometry now in effect.

    Examples:
        >>> set_plot_options(width=8, height=5, dpi=150)
    """
    # Create values dict
    values = {
        "width": width,
        "height": height,
        "dpi": dpi,
    }

    # Filter out None values
    values = {key: value for key, value in values.items() if value is not None}

    # Create options
    options = PlotOptions(
        **{
            **_from_host(),
            **_from_knitr(),
            **_overrides,
            **values,
        },
    )

    # Update overrides
    _overrides.update(values)

    # Return!
    return options


def reset_plot_options() -> PlotOptions:
    """Discard the plot options set through `set_plot_options`.

    Returns:
        PlotOptions: The plot options now in effect.
    """
    # Clear overrides
    _overrides.clear()

    # Return!
    return get_plot_options()
