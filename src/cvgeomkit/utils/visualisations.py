import matplotlib.pyplot as plt

import numpy as np
from cvgeomkit.common import ArrayLike


def display_img(img: ArrayLike) -> None:
    """
    Display an image using matplotlib.
    
    This function provides a simple wrapper around matplotlib's imshow and show
    for displaying images. Uses the global matplotlib configuration set in src.config.
    
    Args:
        img: Image to display (numpy array or NumpyImage)
    
    Note:
        The default colormap is configured globally in src.config.py.
        To use a different colormap for a specific image, use matplotlib directly:
        plt.imshow(img, cmap='your_cmap')
    """
    plt.imshow(img)
    plt.show()


def mask_line_neighborhood_on_edges(
    img: ArrayLike,
    edges: ArrayLike,
    mask: ArrayLike,
) -> ArrayLike:
    """Visualize edges, a line-neighborhood mask, and their overlap for debugging.

    Used only in debug mode to inspect which edge pixels fall inside the boolean
    mask band around a candidate line (e.g. in `filter_horizontal_lines`).
    Edges are drawn white, masked area yellow, and their intersection red.

    Args:
        img (ArrayLike): Reference image used only for its shape.
        edges (ArrayLike): Binary edge map (e.g. from Canny).
        mask (ArrayLike): Boolean mask marking the line's neighborhood.

    Returns:
        ArrayLike: RGB visualization image.
    """
    mask_img = np.zeros_like(img)
    mask_img[edges > 0] = (255, 255, 255)
    mask_img[mask] = (255, 255, 0)
    mask_img = np.where(np.dstack([edges & mask] * 3), (255, 0, 0), mask_img)
    return mask_img

