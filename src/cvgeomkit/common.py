from abc import ABC, abstractmethod
from collections.abc import Hashable as SupportsHash
from enum import StrEnum
from typing import Self

import cv2
import numpy as np
from PIL import Image


type ArrayLike = np.ndarray | NumpyImage


type Numeric = float | int


class BBoxFmt(StrEnum):
    XYWH = "xywh"
    XYXY = "xyxy"
    CXCYWH = "cxcxywh"


class ColorSpace(StrEnum):
    GRAY = "gray"
    BGR = "bgr"
    RGB = "rgb"
    HSV = "hsv"


class NumpyImage(np.ndarray):
    """
    A lightweight wrapper around `numpy.ndarray` for easier image shape handling.

    Provides convenient properties to access image dimensions:
    - `height`: number of rows
    - `width`: number of columns
    - `depth`: number of channels (defaults to 1 if not present)

    Fully compatible with OpenCV and other libraries that expect a standard
    NumPy array, since it is implemented as a view of the original array.

    Use :meth:`to_colorspace` with explicit ``src_space`` and ``dst_space`` (:class:`ColorSpace`)
    to convert between ``gray``, ``bgr``, ``rgb``, and ``hsv`` via OpenCV.
    """
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def to_colorspace(self, dst_space: ColorSpace, src_space: ColorSpace) -> Self:

        if src_space == dst_space:
            return self.copy().view(NumpyImage)

        conversions = {
            (ColorSpace.BGR, ColorSpace.RGB): cv2.COLOR_BGR2RGB,
            (ColorSpace.RGB, ColorSpace.BGR): cv2.COLOR_RGB2BGR,

            (ColorSpace.BGR, ColorSpace.GRAY): cv2.COLOR_BGR2GRAY,
            (ColorSpace.GRAY, ColorSpace.BGR): cv2.COLOR_GRAY2BGR,

            (ColorSpace.RGB, ColorSpace.GRAY): cv2.COLOR_RGB2GRAY,
            (ColorSpace.GRAY, ColorSpace.RGB): cv2.COLOR_GRAY2RGB,

            (ColorSpace.BGR, ColorSpace.HSV): cv2.COLOR_BGR2HSV,
            (ColorSpace.HSV, ColorSpace.BGR): cv2.COLOR_HSV2BGR,

            (ColorSpace.RGB, ColorSpace.HSV): cv2.COLOR_RGB2HSV,
            (ColorSpace.HSV, ColorSpace.RGB): cv2.COLOR_HSV2RGB,
        }

        code = conversions.get((src_space, dst_space))
        if code is None:
            raise ValueError(
                f"Unsupported conversion: {src_space} -> {dst_space}"
            )

        return cv2.cvtColor(self, code).view(NumpyImage)

    @property
    def width(self):
        return self.shape[1] if len(self.shape) > 1 else 1
    
    @property
    def height(self):
        return self.shape[0]
    
    @property
    def depth(self):
        return self.shape[2] if len(self.shape) > 2 else 1
    
    def as_array(self):
        """Convert back to regular numpy array for compatibility"""
        return np.asarray(self)

    @property
    def as_pil(self) -> Image.Image:
        return Image.fromarray(self.as_array())


class Hashable(ABC):
    @abstractmethod
    def _key_(self) -> SupportsHash:
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self._key_())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._key_() == other._key_()