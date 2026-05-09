import numpy as np
from shapely.geometry import Polygon
from cvgeomkit.common import Numeric
from cvgeomkit.geometry.points import Point
from .helpers import order_clockwise


def iou(
    area1: list[list[Numeric]] | list[Point] | np.ndarray,
    area2: list[list[Numeric]] | list[Point] | np.ndarray,
) -> float:

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
    return np.linalg.norm(np.array(point1) - np.array(point2))