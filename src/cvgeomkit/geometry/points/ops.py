from cvgeomkit.geometry.points.point import Point
from cvgeomkit.geometry.intersections.intersection import Intersection


def transform_point(
    point: Intersection | Point,
    original_x_start: int, 
    original_y_start: int, 
    to_global: bool = True
) -> Point:
    """
    Transforms a point's coordinates between local and global image reference frames.

    The function shifts a point by the provided (x, y) offsets depending on the
    transformation direction. Works with both `Point` and `Intersection` objects.

    Args:
        point (Intersection | Point): Point or intersection to transform.
        original_x_start (int): X-axis offset.
        original_y_start (int): Y-axis offset.
        to_global (bool, optional): If True, converts from local to global coordinates;
                                    if False, converts from global to local (default: True).

    Returns:
        Point: Transformed point with updated coordinates.
    """
    
    if isinstance(point, Intersection):
        point = point.point

    if to_global:
        return Point(point.x + original_x_start, point.y + original_y_start)
    else:
        return Point(point.x - original_x_start, point.y - original_y_start)