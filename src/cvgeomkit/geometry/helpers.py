from cvgeomkit.geometry.points.point import Point
from cvgeomkit.geometry.intersections.intersection import Intersection
from cvgeomkit.geometry.lines.segment import LineSegment


def point_in_segment(
    point: Point | Intersection, 
    segment: LineSegment
) -> bool:
    """
    Check if a point is within the bounds of a line segment.
    If an instance of Intersection class is passed, the function will use its `point` attribute for the check.
    This function ensures that both start and end points of the line segment are ordered correctly. 

    Args:
        point: The point or intersection to check.
        segment: The line segment to check against.

    Returns:
        True if the point is within the segment bounds, False otherwise.
    """
    if isinstance(point, Intersection):
        point = point.point
        
    return (min(segment.start.x, segment.end.x) <= point.x <= max(segment.start.x, segment.end.x) and
            min(segment.start.y, segment.end.y) <= point.y <= max(segment.start.y, segment.end.y))