import numpy as np

from cvgeomkit.common import NumpyImage


type ArrayLike = np.ndarray | NumpyImage
type Numeric = float | int
type CollectionLike[T] = list[T] | tuple[T, ...] | set[T]
