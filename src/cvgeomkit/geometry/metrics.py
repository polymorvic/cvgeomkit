import numpy as np
from shapely.geometry import Polygon
from cvgeomkit.types import Numeric
from cvgeomkit.geometry.lines.segment import LineSegment
from cvgeomkit.geometry.points.point import Point
from cvgeomkit.utils.helpers import order_clockwise


def iou(
    area1: list[list[Numeric]] | list[Point] | np.ndarray,
    area2: list[list[Numeric]] | list[Point] | np.ndarray,
) -> float:
    """
    Intersection-over-union of two polygons given as vertex rings.

    Vertices are oriented consistently via :func:`~cvgeomkit.utils.helpers.order_clockwise`
    before building Shapely polygons.
    """
    area1 = order_clockwise(area1)
    area2 = order_clockwise(area2)

    area1 = Polygon(area1)
    area2 = Polygon(area2)

    intersection = area1.intersection(area2).area
    union = area1.union(area2).area

    return intersection / union if union > 0 else 0.0


def euclidean_distance(
        point1: Point | np.ndarray | list[Numeric], 
        point2: Point | np.ndarray | list[Numeric]
) -> float:
    """Euclidean distance between two 2D points (each as ``Point``, array, or pair of numbers)."""
    return np.linalg.norm(np.array(point1) - np.array(point2))



def get_intercept_std(
    line_segments: list[LineSegment]
) -> float:
    intercepts = [
        segment.line.intercept
        for segment in line_segments
    ]

    return float(np.std(intercepts))