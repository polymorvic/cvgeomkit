import cv2
import numpy as np

from cvgeomkit.geometry.lines.segment import LineSegment
from cvgeomkit.geometry.intersections.intersection import Intersection
from cvgeomkit.types import CollectionLike, ArrayLike
from cvgeomkit.geometry.lines.line import Line
from cvgeomkit.geometry.points.point import Point
from cvgeomkit.geometry.points.ops import transform_point
from cvgeomkit.validators import check_if_numpy_image
from cvgeomkit.config.debug import get_debug_mode
from cvgeomkit.utils.visualisations import display_img
from numpy.typing import NDArray


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
    segments1: list[LineSegment], segments2: list[LineSegment], img: ArrayLike
) -> Intersection | None:
    pass


def lines_from_gray_img(
    img: ArrayLike,
    canny_lower_thresh: int,
    canny_upper_thresh: int,
    hough_thresh: int,
    min_line_len_px: int,
    max_line_gap_px: int,
    return_canny: bool = False,
) -> list[Line] | tuple[list[Line], NDArray]:
    img = check_if_numpy_image(img)
    edges = cv2.Canny(img, canny_lower_thresh, canny_upper_thresh)
    segments = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=hough_thresh,
        minLineLength=min_line_len_px,
        maxLineGap=max_line_gap_px,
    )

    if get_debug_mode():
        display_img(edges)
        img_copy = cv2.merge([img, img, img])
        if segments is not None:
            for segment in segments:
                x1, y1, x2, y2 = segment[0]
                cv2.line(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        display_img(img_copy)

    if segments is None:
        return []

    if return_canny:
        return [Line.from_hough_segment(*segment) for segment in segments], edges
    return [Line.from_hough_segment(*segment) for segment in segments]
