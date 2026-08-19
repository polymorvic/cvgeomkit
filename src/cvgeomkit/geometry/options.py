from enum import StrEnum


class Direction(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class Axis(StrEnum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class LinePosition(StrEnum):
    TOP = "top"
    BOTTOM = "bottom"


class ColorSpace(StrEnum):
    GRAY = "gray"
    BGR = "bgr"
    RGB = "rgb"
    HSV = "hsv"
