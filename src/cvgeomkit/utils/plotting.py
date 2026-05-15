import matplotlib.pyplot as plt

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