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

"""Image utilities."""

import matplotlib.pyplot as plt
from PIL import Image


def show_local_image(image_path: str) -> None:
    """Displays a local image using matplotlib.

    Args:
        image_path (str): The file path to the image to be displayed.

    Returns:
        None: Nothing.
    """
    # load and crop image
    img = Image.open(image_path)
    img = img.crop(img.getbbox())

    # define figure object
    plt.figure(figsize=(7, 5), dpi=300)

    # show image in the figure canvas
    plt.imshow(img)

    # configure layout
    plt.axis("off")
    plt.tight_layout()

    # show image!
    plt.show()
