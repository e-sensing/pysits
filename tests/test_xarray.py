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

"""Unit tests for xarray export operations."""

import sys

import numpy as np
import pytest
import rasterio
import xarray as xr
from affine import Affine
from dask.array import Array as DaskArray
from rasterio.crs import CRS
from rasterio.windows import Window

from pysits.sits.context import samples_l8_rondonia_2bands
from pysits.sits.cube import sits_cube
from pysits.sits.data import sits_bbox
from pysits.sits.exporters.xarray import sits_as_xarray
from pysits.sits.utils import r_package_dir

#
# Size and block size of the cube created to test how data is read
#
COG_SIZE = 4000
COG_BLOCK = 512

#
# Grid of the cube created to test how data is read
#
COG_CRS = "EPSG:32620"
COG_RESOLUTION = 10.0
COG_TRANSFORM = Affine(
    a=COG_RESOLUTION,
    b=0.0,
    c=300000.0,
    d=0.0,
    e=-COG_RESOLUTION,
    f=8000000.0,
)

#
# Dates of the cube created to test how data is read
#
COG_DATES = ("2020-01-01", "2020-01-16")


#
# Auxiliary functions
#
def _mod13q1_cube():
    """Create a cube from the local MOD13Q1 files."""
    return sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=r_package_dir("extdata/raster/mod13q1", package="sits"),
        progress=False,
    )


def _class_cube():
    """Create a cube from the local classification files."""
    return sits_cube(
        source="MPC",
        collection="SENTINEL-2-L2A",
        data_dir=r_package_dir("extdata/raster/classif", package="sits"),
        parse_info=("X1", "X2", "tile", "start_date", "end_date", "band", "version"),
        bands="class",
        labels={
            "1": "ClearCut_Fire",
            "2": "ClearCut_Soil",
            "3": "ClearCut_Veg",
            "4": "Forest",
        },
        progress=False,
    )


def _probs_cube(labels=None):
    """Create a cube from the local probability files."""
    return sits_cube(
        source="BDC",
        collection="MOD13Q1-6.1",
        data_dir=r_package_dir("extdata/raster/probs", package="sits"),
        parse_info=("tile", "X2", "band", "start_date", "end_date", "version"),
        bands="probs",
        labels=labels or {str(i): f"class_{i}" for i in range(1, 10)},
        progress=False,
    )


def _first_cube_file(cube):
    """Get the first file of a cube."""
    files = cube["file_info"].tolist()[0]
    files = files.sort_values(files.columns[1]).reset_index(drop=True)

    return str(files.iloc[0]["path"])


class _ReadCounter:
    """Count how much data is read from files."""

    def __init__(self, monkeypatch):
        """Initializer."""
        self.opens = []
        self.pixels = 0

        original_open = rasterio.open
        original_read = rasterio.DatasetReader.read

        def counting_open(*args, **kwargs):
            self.opens.append(str(args[0]) if args else "")

            return original_open(*args, **kwargs)

        def counting_read(reader, *args, **kwargs):
            values = original_read(reader, *args, **kwargs)

            if np.ndim(values) >= 2:  # noqa: PLR2004
                self.pixels += int(np.shape(values)[-1] * np.shape(values)[-2])

            return values

        monkeypatch.setattr(rasterio, "open", counting_open)
        monkeypatch.setattr(rasterio.DatasetReader, "read", counting_read)

    def reset(self):
        """Reset counters."""
        self.opens = []
        self.pixels = 0


@pytest.fixture(scope="session")
def cog_cube_dir(tmp_path_factory):
    """Create a directory."""
    data_dir = tmp_path_factory.mktemp("cog-cube")

    for index, date in enumerate(COG_DATES):
        values = (
            np.arange(COG_SIZE * COG_SIZE).reshape(COG_SIZE, COG_SIZE) + index * 7
        ) % 10000

        # Value as int16
        values = values.astype("int16")

        with rasterio.open(
            fp=data_dir / f"SENTINEL-2_MSI_20LLQ_B02_{date}.tif",
            mode="w",
            driver="GTiff",
            height=COG_SIZE,
            width=COG_SIZE,
            count=1,
            dtype="int16",
            crs=CRS.from_string(COG_CRS),
            transform=COG_TRANSFORM,
            nodata=-9999,
            tiled=True,
            blockxsize=COG_BLOCK,
            blockysize=COG_BLOCK,
        ) as dataset:
            dataset.write(values, 1)

    return data_dir


@pytest.fixture
def cog_cube(cog_cube_dir):
    """Create a cube."""
    return sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        data_dir=cog_cube_dir.as_posix(),
        parse_info=("X1", "X2", "tile", "band", "date"),
        bands="B02",
        progress=False,
    )


#
# Data cubes
#
def test_xarray_cube_dimensions():
    """Test cube conversion dimensions and coordinates."""
    data = sits_as_xarray(_mod13q1_cube())

    assert isinstance(data, xr.DataArray)
    assert data.dims == ("band", "time", "y", "x")

    # Shape comes from the cube files
    assert data.sizes == {"band": 1, "time": 12, "y": 147, "x": 255}
    assert list(data["band"].values) == ["NDVI"]

    # Band configuration is available to users
    assert data["scale_factor"].item() == pytest.approx(0.0001)
    assert data["missing_value"].item() == -3000  # noqa: PLR2004

    # Data is georeferenced
    assert data.rio.crs is not None
    assert "spatial_ref" in data.coords


def test_xarray_cube_values():
    """Test cube conversion values, against the values in the files."""
    cube = _mod13q1_cube()
    data = sits_as_xarray(cube)

    with rasterio.open(_first_cube_file(cube)) as dataset:
        expected = dataset.read(1).astype("float32")
        expected_transform = dataset.transform

    # Missing values are removed, and values are scaled
    expected = np.where(expected == -3000, np.nan, expected) * 0.0001  # noqa: PLR2004

    # Get NDVI value
    values = data.sel(band="NDVI").isel(time=0).compute()

    # Test type and values
    assert values.dtype == np.dtype("float32")
    assert np.allclose(values.values, expected, equal_nan=True)

    # Values are in their physical range
    assert -1 <= float(values.min()) <= float(values.max()) <= 1

    # Data is aligned with the files
    assert data.rio.transform().c == pytest.approx(expected_transform.c)
    assert data.rio.transform().f == pytest.approx(expected_transform.f)


def test_xarray_cube_without_scale():
    """Test cube conversion without scaling."""
    cube = _mod13q1_cube()
    data = sits_as_xarray(cube, scale=False)

    with rasterio.open(_first_cube_file(cube)) as dataset:
        expected = dataset.read(1)

    # Test with NDVI
    values = data.sel(band="NDVI").isel(time=0).compute()

    # Values keep their original type and range
    assert values.dtype == expected.dtype
    assert np.array_equal(values.values, expected)


def test_xarray_cube_bands():
    """Test cube conversion with band selection."""
    cube = _mod13q1_cube()
    data = sits_as_xarray(cube, bands=["NDVI"])

    assert list(data["band"].values) == ["NDVI"]

    with pytest.raises(ValueError, match="Bands not available"):
        sits_as_xarray(cube, bands=["EVI"])


#
# Lazy access
#
def test_xarray_cube_is_lazy(cog_cube, monkeypatch):
    """Test that cube conversion doesn't read data from files."""
    counter = _ReadCounter(monkeypatch)

    data = sits_as_xarray(cog_cube)

    # Building the cube uses only metadata
    assert counter.opens == []
    assert counter.pixels == 0

    # Data is available as chunks, and is read only when required
    assert isinstance(data.data, DaskArray)
    assert data.chunksizes["x"][0] == COG_BLOCK
    assert data.chunksizes["y"][0] == COG_BLOCK


def test_xarray_cube_reads_windows(cog_cube, monkeypatch):
    """Test that only the required data is read from files."""
    counter = _ReadCounter(monkeypatch)

    # Transform
    data = sits_as_xarray(cog_cube, scale=False)

    # Reset
    counter.reset()

    # Select
    values = data.isel(
        band=0,
        time=0,
        y=slice(0, 10),
        x=slice(0, 10),
    )
    values = values.compute()

    # Values must be small block
    assert len(counter.opens) == 1
    assert counter.pixels <= COG_BLOCK * COG_BLOCK
    assert counter.pixels < COG_SIZE * COG_SIZE

    # Load window
    with rasterio.open(_first_cube_file(cog_cube)) as dataset:
        expected = dataset.read(1, window=Window(0, 0, 10, 10))

    # Both must be the same
    assert np.array_equal(values.values, expected)


def test_xarray_cube_chunks(cog_cube):
    """Test cube conversion with user-defined chunks."""
    data = sits_as_xarray(cog_cube, chunks={"x": 1024, "y": 1024})

    assert data.chunksizes["x"][0] == 1024  # noqa: PLR2004
    assert data.chunksizes["y"][0] == 1024  # noqa: PLR2004


#
# Derived cubes
#
def test_xarray_class_cube():
    """Test class cube conversion."""
    cube = _class_cube()
    data = sits_as_xarray(cube)

    # Test metadata
    assert isinstance(data, xr.DataArray)
    assert data.dims == ("y", "x")

    # Test data properties
    assert data.dtype == np.dtype("uint8")
    assert data.attrs["labels"] == {
        1: "ClearCut_Fire",
        2: "ClearCut_Soil",
        3: "ClearCut_Veg",
        4: "Forest",
    }

    # Load data
    with rasterio.open(_first_cube_file(cube)) as dataset:
        expected = dataset.read(1)

    # Values must be the same
    assert np.array_equal(data.compute().values, expected)

    # Derived cubes describe a period
    assert data.attrs["start_date"] == "2020-06-04"
    assert data.attrs["end_date"] == "2021-08-26"


def test_xarray_probs_cube():
    """Test probability cube conversion."""
    data = sits_as_xarray(_probs_cube())

    # Test type and properties
    assert isinstance(data, xr.DataArray)
    assert data.dims == ("label", "y", "x")
    assert list(data["label"].values) == [f"class_{i}" for i in range(1, 10)]

    # Probabilities are scaled
    assert data.dtype == np.dtype("float32")
    assert 0 <= float(data.min()) <= float(data.max()) <= 1


def test_xarray_probs_cube_invalid_labels():
    """Test probability cube conversion with invalid labels."""
    cube = _probs_cube(labels={"1": "Cerrado", "2": "Forest"})

    with pytest.raises(ValueError, match="labels"):
        sits_as_xarray(cube)


def test_xarray_derived_cube_bands():
    """Test that bands are not available for derived cubes."""
    with pytest.raises(ValueError, match="derived from a classification"):
        sits_as_xarray(_class_cube(), bands=["class"])


#
# Time series
#
def test_xarray_time_series():
    """Test time series conversion."""
    data = sits_as_xarray(samples_l8_rondonia_2bands)

    # Test type and properties
    assert isinstance(data, xr.Dataset)
    assert data.sizes == {"sample": 160, "time": 25}
    assert all(band in data for band in ["EVI", "NDVI"])

    # Sample metadata is available to users
    assert all(
        coord in data.coords for coord in ["longitude", "latitude", "label", "cube"]
    )


def test_xarray_time_series_bands():
    """Test time series conversion with band selection."""
    data = sits_as_xarray(samples_l8_rondonia_2bands, bands=["NDVI"])

    # Ensure bands are correctly selected
    assert "NDVI" in data
    assert "EVI" not in data

    # Invalid band must produce an error
    with pytest.raises(ValueError, match="Bands not available"):
        sits_as_xarray(samples_l8_rondonia_2bands, bands=["B02"])


def test_xarray_time_series_different_timelines():
    """Test time series conversion with samples of different timelines."""
    samples = samples_l8_rondonia_2bands.copy()

    # Remove a date from the first sample
    time_series = samples["time_series"].tolist()
    time_series[0] = time_series[0].iloc[1:].reset_index(drop=True)
    samples["time_series"] = time_series

    # Transform
    data = sits_as_xarray(samples)

    # Samples are aligned by date, and dates without data are empty
    assert data.sizes == {"sample": 160, "time": 25}
    assert bool(np.isnan(data["NDVI"].isel(sample=0, time=0)))
    assert not bool(np.isnan(data["NDVI"].isel(sample=1, time=0)))


def test_xarray_time_series_cube_arguments():
    """Test that cube arguments are not available for time series."""
    with pytest.raises(ValueError, match="only available for data cubes"):
        sits_as_xarray(samples_l8_rondonia_2bands, chunks={"x": 512})

    with pytest.raises(ValueError, match="only available for data cubes"):
        sits_as_xarray(samples_l8_rondonia_2bands, cube_args={"resampling": "bilinear"})


#
# Errors
#
def test_xarray_unsupported_data():
    """Test conversion of data without an xarray representation."""
    with pytest.raises(NotImplementedError, match="sits_as_xarray"):
        sits_as_xarray(sits_bbox(samples_l8_rondonia_2bands))


def test_xarray_without_dependencies(monkeypatch):
    """Test conversion when the xarray dependencies are not installed."""
    monkeypatch.setitem(sys.modules, "pysits.conversions.xarray", None)

    with pytest.raises(ImportError, match=r"pysits\[xarray\]"):
        sits_as_xarray(samples_l8_rondonia_2bands)


#
# Cubes with multiple grids
#
def test_xarray_cube_multiple_grids():
    """Test conversion of a cube with bands in different resolutions."""
    cube = sits_cube(
        source="AWS",
        collection="SENTINEL-2-L2A",
        tiles="20LLQ",
        bands=("B02", "B11"),
        start_date="2020-01-01",
        end_date="2020-01-20",
        progress=False,
    )

    data = sits_as_xarray(cube)

    # Bands in different grids are not resampled: each grid is a node
    assert isinstance(data, xr.DataTree)
    assert sorted(data.children) == ["epsg32720-10m", "epsg32720-20m"]

    # Get bands
    band_10m = data["epsg32720-10m"].ds["cube"]
    band_20m = data["epsg32720-20m"].ds["cube"]

    # Test properties
    assert list(band_10m["band"].values) == ["B02"]
    assert list(band_20m["band"].values) == ["B11"]

    # Each node keeps the native grid of its files
    assert band_10m.sizes["x"] == 10980  # noqa: PLR2004
    assert band_20m.sizes["x"] == 5490  # noqa: PLR2004
