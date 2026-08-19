import numpy as np

from cvgeomkit.common import NumpyImage
from cvgeomkit.errors import NotArrayError
from cvgeomkit.types import ArrayLike, CollectionLike


def check_if_numpy_image(img: ArrayLike) -> NumpyImage:
    """Validate and return the input as a NumpyImage.

    Args:
        img (ArrayLike): A NumpyImage instance or a NumPy array to convert.

    Raises:
        NotArrayError: If the input is neither a NumpyImage nor a NumPy array.

    Returns:
        NumpyImage: The original NumpyImage or a NumpyImage created from the array.
    """

    if isinstance(img, NumpyImage):
        return img

    if isinstance(img, np.ndarray):
        return NumpyImage(img)

    raise NotArrayError()


def exceeds_empty_threshold(values: CollectionLike, threshold: float) -> bool:
    """Check whether empty values meet the specified threshold.

    Args:
        values (CollectionLike): Values to check for empty elements represented by None.
        threshold (float): Minimum empty-value ratio, from 0 to 1.

    Returns:
        bool: True if the ratio of None values is at least the threshold.
    """
    empty_count = sum(v is None for v in values)
    return empty_count / len(values) >= threshold if values else False
