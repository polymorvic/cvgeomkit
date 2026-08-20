import matplotlib.pyplot as plt


def set_cmap_gray() -> None:
    """Set the default colormap to grayscale for matplotlib plots."""
    plt.rcParams['image.cmap'] = 'gray'

