from pathlib import Path
from typing import Literal, Sequence

import cv2
import numpy as np

from cvgeomkit.common import BBoxFmt, NumpyImage
from cvgeomkit.geometry.points import Point
from cvgeomkit.geometry.lines import LineGroup, Line


def convert_bbox(
    bbox: Sequence,
    to_fmt: BBoxFmt,
    returns_int: bool = True,
) -> tuple[int, int, int, int] | tuple[float, float, float, float]:
    if to_fmt == BBoxFmt.XYXY:
        x, y, w, h = bbox
        out = (x, y, x + w, y + h)
    else:
        x1, y1, x2, y2 = bbox
        out = (x1, y1, x2 - x1, y2 - y1)

    if returns_int:
        return tuple(map(int, out))
    return out


def rerange_hue(hue: np.ndarray) -> float:
    """
    Shifts the hue channel by 90 with wrap-around (overflow) within the 0–179 range.
    Uses modulo arithmetic to keep the result within the valid hue range
    """
    return (hue + 90) % 180


def group_lines(lines: list[Line], 
    thresh_theta: float | int = 5, 
    thresh_intercept: float | int = 10
    ) -> list[LineGroup]:
    """
    Group similar Line objects into LineGroups based on orientation and position thresholds.

    Args:
        lines (list[Line]): A list of Line objects to group.
        thresh_theta (float): Maximum allowed angle difference between lines to be in the same group.
        thresh_intercept (float): Maximum allowed intercept difference (for non-vertical lines).

    Returns:
        list[LineGroup]: A list of LineGroup objects representing grouped lines.
    """
    groups = []

    for line in lines:
        for group in groups:
            if group.process_line(line, thresh_theta, thresh_intercept):
                break
        else:
            groups.append(LineGroup([line]))

    return groups


def read_image_as_numpyimage(path: str | Path, color_mode: Literal["rgb", "hsv", "grayscale"] = "rgb") -> NumpyImage:
    color_mode = color_mode.lower()
    if color_mode not in {"rgb", "hsv", "grayscale"}:
        raise ValueError("color_mode must be 'RGB', 'HSV', or 'GRAYSCALE'")

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE if color_mode == "grayscale" else cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {path}")

    conversions = {
        "rgb": lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2RGB),
        "hsv": lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2HSV),
    }

    img = conversions.get(color_mode, lambda x: x)(img)
    return NumpyImage(img)


def order_clockwise(points):
    if isinstance(points, np.ndarray):
        arr = np.asarray(points, dtype=float)

    elif points and isinstance(points[0], Point):
        arr = np.array([[p.x, p.y] for p in points], dtype=float)

    else:
        arr = np.asarray(points, dtype=float)

    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError("points must be of shape (N, 2)")

    if len(arr) < 3:
        return arr

    center = arr.mean(axis=0)
    angles = np.arctan2(arr[:, 1] - center[1], arr[:, 0] - center[0])

    return arr[np.argsort(-angles)]