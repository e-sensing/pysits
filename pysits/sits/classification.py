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

"""Classification operations."""

from pysits.backend.pkgs import r_pkg_sits
from pysits.conversions.decorators import function_call
from pysits.docs import attach_doc
from pysits.models.data.cube import SITSCubeModel
from pysits.models.resolver import resolve_and_invoke_content_class


@function_call(r_pkg_sits.sits_classify, resolve_and_invoke_content_class)
@attach_doc("sits_classify")
def sits_classify(*args, **kwargs) -> SITSCubeModel:
    """Classify data."""


@function_call(r_pkg_sits.sits_smooth, SITSCubeModel)
@attach_doc("sits_smooth")
def sits_smooth(*args, **kwargs) -> SITSCubeModel:
    """Smooth classification data."""


@function_call(r_pkg_sits.sits_label_classification, SITSCubeModel)
@attach_doc("sits_label_classification")
def sits_label_classification(*args, **kwargs) -> SITSCubeModel:
    """Label probabilities data."""
