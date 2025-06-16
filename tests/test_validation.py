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

"""Unit tests for validation operations (cube and time-series)."""

from pysits.models.data.matrix import SITSConfusionMatrix
from pysits.models.data.table import SITSTable
from pysits.models.data.vector import SITSNamedVector
from pysits.sits.context import cerrado_2classes
from pysits.sits.ml import sits_rfor
from pysits.sits.ts import sits_sample, sits_validate


def test_sits_validate():
    """Test validate operation."""

    # Sample data
    samples = sits_sample(cerrado_2classes, frac=0.5)
    samples_validation = sits_sample(cerrado_2classes, frac=0.5)

    # Validate samples
    matrix = sits_validate(
        samples=samples, samples_validation=samples_validation, ml_method=sits_rfor()
    )

    # Check properties
    assert isinstance(matrix, SITSConfusionMatrix)
    assert isinstance(matrix.by_class, SITSNamedVector)
    assert isinstance(matrix.dots, list)
    assert isinstance(matrix.mode, str)
    assert isinstance(matrix.overall, SITSNamedVector)
    assert isinstance(matrix.table, SITSTable)

    # Check values
    assert matrix.mode == "sens_spec"
    assert matrix.positive == "Cerrado"
