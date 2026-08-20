from cvgeomkit.geometry.lines.segment import LineSegment
from cvgeomkit.geometry.intersections.intersection import Intersection
from cvgeomkit.types import CollectionLike, ArrayLike
from cvgeomkit.geometry.lines.line import Line
from cvgeomkit.geometry.points.point import Point
from cvgeomkit.geometry.points.ops import transform_point


def transform_line(
    original_line: Line,
    original_img: ArrayLike,
    original_x_start: int,
    original_y_start: int,
    to_global: bool = True,
) -> Line:
    """
    Transforms a line's coordinates between local and global image reference frames.

    The function shifts both endpoints of a line by the provided offsets using
    `transform_point` and reconstructs a new line from the transformed coordinates.

    Args:
        original_line (Line): Line object to transform.
        original_img (np.ndarray): Image used to determine line limits.
        original_x_start (int): X-axis offset.
        original_y_start (int): Y-axis offset.
        to_global (bool, optional): If True, converts from local to global coordinates;
                                    if False, converts from global to local (default: True).

    Returns:
        Line: Transformed line object with updated coordinates.
    """
    pts_source: CollectionLike[Point] = original_line.limit_to_img(original_img)
    pts_transformed = [
        transform_point(p, original_x_start, original_y_start, to_global=to_global)
        for p in pts_source
    ]
    return Line.from_points(*pts_transformed)


def transform_line_segment(
    segment: LineSegment,
    original_x_start: int,
    original_y_start: int,
    to_global: bool = True,
) -> LineSegment:
    start = transform_point(
        segment.start,
        original_x_start,
        original_y_start,
        to_global=to_global,
    )
    end = transform_point(
        segment.end,
        original_x_start,
        original_y_start,
        to_global=to_global,
    )
    return LineSegment(start, end)


def line_segments_intersections(
    segments1: list[LineSegment],
    segments2: list[LineSegment],
    img: ArrayLike
) -> Intersection | None:
    pass
