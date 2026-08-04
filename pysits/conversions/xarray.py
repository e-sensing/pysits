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

"""Xarray conversions."""

from __future__ import annotations

import numpy as np
import rioxarray as xrio
import xarray as xr
from odc.stac import load as odc_load
from pandas import DataFrame as PandasDataFrame
from pandas import concat as pandas_concat

from pysits.conversions.stac import (
    files_geobox,
    grid_group_name,
    signature_file_url,
    stac_items_from_files,
)
from pysits.models.data.base import SITSData
from pysits.models.data.cube import SITSCubeModel
from pysits.sits.config import sits_config_value
from pysits.sits.data import sits_labels

#
# Data types used by sits, and their numpy equivalents
#
DATA_TYPES = {
    "INT1U": "uint8",
    "INT1S": "int8",
    "INT2U": "uint16",
    "INT2S": "int16",
    "INT4U": "uint32",
    "INT4S": "int32",
    "FLT4S": "float32",
    "FLT8S": "float64",
}

#
# Default chunks used to read data cubes
#
DEFAULT_CHUNKS = {"x": 512, "y": 512}

#
# Name of the variable used in nodes of a data tree
#
TREE_VARIABLE = "cube"


#
# Cube files
#
def cube_files(cube: SITSCubeModel) -> PandasDataFrame:
    """Merge the ``file_info`` of all cube rows, keeping tile metadata.

    Args:
        cube (SITSCubeModel): Data cube.

    Returns:
        PandasDataFrame: All cube files in a single data frame.
    """
    files = []

    for _, cube_row in cube.iterrows():
        file_info = cube_row["file_info"].copy()

        file_info["crs"] = str(cube_row["crs"])
        file_info["tile"] = str(cube_row["tile"])

        files.append(file_info)

    # Return!
    return pandas_concat(files, ignore_index=True)


def cube_grid_groups(
    cube: SITSCubeModel, bands: list[str] | None = None
) -> dict[tuple, PandasDataFrame]:
    """Group cube files by grid.

    Files are grouped by CRS and resolution. Files of a group share a grid, and
    can be read together without resampling.

    Args:
        cube (SITSCubeModel): Data cube.

        bands (list[str]): Bands to use. When ``None``, all bands are used.

    Returns:
        dict[tuple, PandasDataFrame]: Files indexed by ``(crs, xres, yres)``.

    Raises:
        ValueError: When a band is not available in the cube.
    """
    files = cube_files(cube)

    # Select bands
    if bands is not None:
        # Get bands available
        available = sorted(files["band"].unique())

        # Get bands not available
        missing_bands = [band for band in bands if band not in available]

        # If user selected any band not available, error
        if missing_bands:
            raise ValueError(
                f"Bands not available in the cube: {', '.join(missing_bands)}. "
                f"Available bands: {', '.join(available)}"
            )

        # Select file of bands
        files = files[files["band"].isin(bands)]

    # Group by grid
    return {
        key: group.reset_index(drop=True)
        for key, group in files.groupby(["crs", "xres", "yres"], sort=True)
    }


#
# Band configuration
#
def _band_config_keys(cube: SITSCubeModel, band: str) -> tuple[str, ...]:
    """Define the configuration keys of a cube band.

    Args:
        cube (SITSCubeModel): Data cube.

        band (str): Band name.

    Returns:
        tuple[str, ...]: Configuration keys of the band.
    """
    classes = list(cube._instance.rclass)

    # Cubes derived from a classification have their
    # own configuration
    if "derived_cube" in classes:
        return ("derived_cube", classes[0], "bands", band)

    return (
        "sources",
        str(cube["source"].iloc[0]),
        "collections",
        str(cube["collection"].iloc[0]),
        "bands",
        band,
    )


def _scaling_required(configs: dict[str, dict]) -> bool:
    """Check if bands require scaling.

    Args:
        configs (dict[str, dict]): Band configurations, indexed by band.

    Returns:
        bool: ``True`` when at least one band has a scale factor or an offset.
    """
    for config in configs.values():
        # Get scale factor
        scale_factor = config["scale_factor"]

        # Get offset value
        offset_value = config["offset_value"]

        # Check which is correct and valid
        is_scale_factor_valid = scale_factor is not None and scale_factor != 1
        is_offset_valid = offset_value is not None and offset_value != 0

        # If at least one is correct
        if is_scale_factor_valid or is_offset_valid:
            # Scalling / offset is required!
            return True

    # Fallback: Scaling is not applied
    return False


def _band_property(configs: dict[str, dict], bands: list[str], prop: str, default):
    """Extract a band property as an array, aligned with ``bands``."""
    return xr.DataArray(
        data=[
            default if configs[band][prop] is None else configs[band][prop]
            for band in bands
        ],
        dims="band",
        coords={"band": bands},
    )


def band_config(cube: SITSCubeModel, band: str) -> dict:
    """Get the configuration of a cube band.

    Args:
        cube (SITSCubeModel): Data cube.

        band (str): Band name.

    Returns:
        dict: Band ``scale_factor``, ``offset_value``, ``missing_value`` and
            ``data_type``.
    """
    keys = _band_config_keys(cube, band)

    return {
        prop: sits_config_value(*keys, prop, default=None)
        for prop in ("scale_factor", "offset_value", "missing_value", "data_type")
    }


def apply_band_scaling(
    data: xr.DataArray, configs: dict[str, dict], scale: bool
) -> xr.DataArray:
    """Apply the sits configuration to cube values.

    Missing values are replaced by ``NaN`` and values are converted to their
    physical range using the band scale factor and offset.

    Args:
        data (xr.DataArray): Cube data, with a ``band`` dimension.

        configs (dict[str, dict]): Band configurations, indexed by band.

        scale (bool): Flag to scale values.

    Returns:
        xr.DataArray: Data with the band configuration applied.
    """
    # Get bands available
    bands = [str(band) for band in data["band"].values]

    # Bands without scaling keep their values and data type (e.g., class cubes)
    if scale and _scaling_required(configs):
        missing_values = _band_property(
            configs=configs,
            bands=bands,
            prop="missing_value",
            default=np.nan,
        )
        scale_factors = _band_property(
            configs=configs,
            bands=bands,
            prop="scale_factor",
            default=1,
        )
        offset_values = _band_property(
            configs=configs,
            bands=bands,
            prop="offset_value",
            default=0,
        )

        # Scale only valid values
        data = data.where(data != missing_values)

        # Scale!
        data = (data * scale_factors + offset_values).astype("float32")

    # Keep the band configuration available to users
    return data.assign_coords(
        {
            "scale_factor": _band_property(
                configs=configs,
                bands=bands,
                prop="scale_factor",
                default=np.nan,
            ),
            "offset_value": _band_property(
                configs=configs,
                bands=bands,
                prop="offset_value",
                default=np.nan,
            ),
            "missing_value": _band_property(
                configs=configs,
                bands=bands,
                prop="missing_value",
                default=np.nan,
            ),
        }
    )


#
# Data cube conversions
#
def _load_grid_group(
    cube: SITSCubeModel,
    files: PandasDataFrame,
    scale: bool,
    chunks: dict,
    cube_args: dict,
) -> xr.DataArray:
    """Load all files of a grid group.

    Args:
        cube (SITSCubeModel): Data cube.

        files (PandasDataFrame): Files of a single grid group.

        scale (bool): Flag to scale values.

        chunks (dict): Chunks used to read data.

        cube_args (dict): Extra arguments used to read data.

    Returns:
        xr.DataArray: Group data, with dimensions ``(band, time, y, x)``.
    """
    bands = sorted(files["band"].unique())
    configs = {band: band_config(cube, band) for band in bands}

    load_args = {
        "chunks": chunks,
        "groupby": "time",
        "fail_on_error": True,
        "geobox": files_geobox(files),
        "patch_url": signature_file_url,
    }

    # Data types and missing values are only used when shared by all bands
    data_types = {configs[band]["data_type"] for band in bands}
    missing_values = {configs[band]["missing_value"] for band in bands}

    # If there is one data type
    if len(data_types) == 1 and None not in data_types:
        # Get dtype
        load_args["dtype"] = DATA_TYPES[data_types.pop()]

        # Only one missing value
        if len(missing_values) == 1 and None not in missing_values:
            # nodata value
            load_args["nodata"] = missing_values.pop()

    # Update args if required
    load_args.update(cube_args)

    # Read files
    data = stac_items_from_files(files)

    # Transform int dataset
    data = odc_load(
        items=data,
        bands=bands,
        **load_args,
    )

    # Transform into dataarray
    data = data.to_dataarray(dim="band")

    # Apply band scalling
    return apply_band_scaling(data, configs, scale)


def raster_cube_as_xarray(
    cube: SITSCubeModel,
    bands: list[str] | None = None,
    scale: bool = True,
    chunks: dict | None = None,
    cube_args: dict | None = None,
) -> xr.DataArray | xr.DataTree:
    """Convert a data cube to xarray.

    Args:
        cube (SITSCubeModel): Data cube.

        bands (list[str]): Bands to use. When ``None``, all bands are used.

        scale (bool): Flag to scale values.

        chunks (dict): Chunks used to read data.

        cube_args (dict): Extra arguments used to read data.

    Returns:
        xr.DataArray | xr.DataTree: Cube data with dimensions ``(band, time, y, x)``.
    """
    arrays = {}
    groups = cube_grid_groups(cube, bands)

    for index, files in enumerate(groups.values()):
        arrays[grid_group_name(files, index)] = _load_grid_group(
            cube=cube,
            files=files,
            scale=scale,
            chunks=chunks or DEFAULT_CHUNKS,
            cube_args=cube_args or {},
        )

    # Cubes in a single grid are represented as arrays
    if len(arrays) == 1:
        return next(iter(arrays.values()))

    return xr.DataTree.from_dict(
        {name: array.to_dataset(name=TREE_VARIABLE) for name, array in arrays.items()}
    )


#
# Derived data cube conversions
#
def _open_derived_file(path: str, chunks: dict | None) -> xr.DataArray:
    """Open a file of a derived cube.

    Args:
        path (str): File path.

        chunks (dict): Chunks used to read data.

    Returns:
        xr.DataArray: File data, with dimensions ``(band, y, x)``.
    """
    return xrio.open_rasterio(signature_file_url(path), chunks=chunks, masked=False)


def _derived_labels(cube: SITSCubeModel) -> list[str]:
    """Get the labels of a derived cube."""
    labels = sits_labels(cube)

    return [str(label) for label in labels]


def _apply_derived_scaling(
    data: xr.DataArray, config: dict, scale: bool
) -> xr.DataArray:
    """Apply the sits configuration to derived cube values.

    Args:
        data (xr.DataArray): Derived cube data.

        config (dict): Band configuration.

        scale (bool): Flag to scale values.

    Returns:
        xr.DataArray: Data with the band configuration applied.
    """
    # Files define their own missing value, which is used when available
    missing_value = data.rio.nodata

    if missing_value is None:
        missing_value = config["missing_value"]

    # Get scale and offset values
    scale_factor = config["scale_factor"]
    offset_value = config["offset_value"]

    # Test values
    has_scale = scale_factor is not None and scale_factor != 1
    has_offset = offset_value is not None and offset_value != 0

    # Has any scaling ?
    has_scaling = has_scale or has_offset

    # If there are scaling: keep training
    if scale and has_scaling:
        if missing_value is not None:
            data = data.where(data != missing_value)

        # Apply scale + offset
        data = data * (scale_factor or 1) + (offset_value or 0)

        # Data as float32
        data = data.astype("float32")

    data.attrs.update(
        {
            "scale_factor": scale_factor,
            "offset_value": offset_value,
            "missing_value": missing_value,
        }
    )

    return data


def derived_cube_as_xarray(
    cube: SITSCubeModel,
    scale: bool = True,
    chunks: dict | None = None,
) -> xr.DataArray | xr.DataTree:
    """Convert a cube derived from a classification to xarray.

    Args:
        cube (SITSCubeModel): Derived data cube (e.g., class, probs).

        scale (bool): Flag to scale values.

        chunks (dict): Chunks used to read data.

    Returns:
        xr.DataArray | xr.DataTree: Cube data. Probability cubes have
            dimensions ``(label, y, x)``, class cubes ``(y, x)``, and the
            remaining derived cubes ``(band, y, x)``. When the cube has files
            in more than one grid, a data tree with one node per grid is
            returned.

    Raises:
        ValueError: When cube labels don't describe the data available in the
            files of the cube.
    """
    arrays = {}
    classes = list(cube._instance.rclass)

    is_probs = "probs_cube" in classes
    is_class = "class_cube" in classes

    groups = cube_grid_groups(cube)

    # For groups defined
    for index, files in enumerate(groups.values()):
        tiles = []

        # Iterate files
        for _, file in files.iterrows():
            band = str(file["band"])
            config = band_config(cube=cube, band=band)

            # Open derived file
            data = _open_derived_file(
                path=str(file["path"]),
                chunks=chunks or DEFAULT_CHUNKS,
            )

            # Case: probs cube
            if is_probs:
                # Get labels
                labels = _derived_labels(cube)

                # If there are more labels than bands, assume there is
                # something wrong
                if data.sizes["band"] != len(labels):
                    raise ValueError(
                        f"Cube has {len(labels)} labels, but its files have "
                        f"{data.sizes['band']} layers. Check the labels used to "
                        "create the cube."
                    )

                # Rename label with band
                data = data.rename({"band": "label"})

                # Add coordinates
                data = data.assign_coords(label=labels)

            # Case: class cube
            elif is_class:
                data = data.squeeze("band", drop=True)

            # Case: Any other case
            else:
                data = data.assign_coords(band=[band])

            # Apply scaling
            data = _apply_derived_scaling(
                data=data,
                config=config,
                scale=scale,
            )

            # Save result
            tiles.append(data)

        # Generate one main array
        array = tiles[0] if len(tiles) == 1 else xr.combine_by_coords(tiles)

        # Keep cube metadata available to users
        array.attrs.update(
            {
                "start_date": str(files["start_date"].min()),
                "end_date": str(files["end_date"].max()),
            }
        )

        # If class, save labels as metadata as well
        if is_class:
            array.attrs["labels"] = dict(enumerate(_derived_labels(cube), start=1))

        # Save grid
        arrays[grid_group_name(files, index)] = array

    # Just return it
    if len(arrays) == 1:
        return next(iter(arrays.values()))

    # If there are more than one array, return a data tree
    return xr.DataTree.from_dict(
        {name: array.to_dataset(name=TREE_VARIABLE) for name, array in arrays.items()}
    )


#
# Time series conversions
#
def time_series_as_xarray(data: SITSData, bands: list[str] | None = None) -> xr.Dataset:
    """Convert time series to xarray.

    Args:
        data (SITSData): Time series data.

        bands (list[str]): Bands to use. When ``None``, all bands are used.

    Returns:
        xr.Dataset: Time series with dimensions ``(sample, time)``. Samples
            with different timelines are aligned, using ``NaN`` in the dates
            they don't have.

    Raises:
        ValueError: When a band is not available in the time series.
    """
    metadata = data.drop(columns="time_series")
    time_series = data["time_series"].tolist()

    # Bands available in the time series
    available_bands = [column for column in time_series[0].columns if column != "Index"]

    if bands is not None:
        missing_bands = [band for band in bands if band not in available_bands]

        if missing_bands:
            raise ValueError(
                f"Bands not available in the time series: {', '.join(missing_bands)}. "
                f"Available bands: {', '.join(available_bands)}"
            )

        available_bands = list(bands)

    # Samples can have different timelines, which are aligned when required
    timelines = [ts["Index"] for ts in time_series]

    # Define the shared timeline dates
    shared_timeline = all(
        len(timeline) == len(timelines[0]) and timeline.equals(timelines[0])
        for timeline in timelines
    )

    # If there are shared dates, stack it
    if shared_timeline:
        # Stack data
        values = [ts[available_bands].to_numpy() for ts in time_series]
        values = np.stack(values)

        # Data as sample
        samples = xr.DataArray(
            values,
            dims=("sample", "time", "band"),
            coords={
                "sample": np.arange(len(time_series)),
                "time": timelines[0],
                "band": available_bands,
            },
        )

    # Otherwise, concat it
    else:
        samples = xr.concat(
            [
                xr.DataArray(
                    data=ts[available_bands].to_numpy(),
                    dims=("time", "band"),
                    coords={"time": ts["Index"], "band": available_bands},
                )
                for ts in time_series
            ],
            dim="sample",
            join="outer",
        )

        # Assign coordinates
        samples = samples.assign_coords(sample=np.arange(len(time_series)))

    # Keep sample metadata available to users
    properties = ("longitude", "latitude", "label", "cube", "start_date", "end_date")

    coords = {
        column: ("sample", metadata[column].to_numpy())
        for column in properties
        if column in metadata.columns
    }

    # Return!
    return samples.assign_coords(coords).to_dataset(dim="band")
