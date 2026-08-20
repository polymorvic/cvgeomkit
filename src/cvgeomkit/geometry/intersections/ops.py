from cvgeomkit.types import ArrayLike

from cvgeomkit.geometry.lines.line import Line
from cvgeomkit.geometry.lines.ops import transform_line
from cvgeomkit.geometry.points.ops import transform_point
from cvgeomkit.geometry.intersections.intersection import Intersection


def compute_intersections(
    lines: list[Line], 
    image: ArrayLike
) -> list[Intersection]:
    """
    Compute all intersection points between pairs of lines within image boundaries.
    
    This function finds all valid intersection points between every pair of lines
    in the provided list that lie within the image boundaries. Each pair of lines
    is checked only once to avoid duplicates.
    
    Args:
        lines: List of Line objects to find intersections between
        image: Image array used to determine valid intersection boundaries
    
    Returns:
        List of Intersection objects representing valid intersection points
    
    Note:
        Only intersections within the image boundaries are included. Each pair
        of lines is processed only once (no duplicates).
    """
    intersections = set()
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            intersection = lines[i].intersection(lines[j], image)
            if intersection is not None:
                intersections.add(intersection)
    return list(intersections)


def transform_intersection(
    intersection: Intersection,
    source_img: ArrayLike,
    original_x_start: int,
    original_y_start: int,
    to_global: bool = True,
) -> Intersection:
    """
    Transforms an Intersection in one go.
    - If to_global=True: treats inputs as LOCAL and returns GLOBAL.
    - If to_global=False: treats inputs as GLOBAL and returns LOCAL.

    Note:
        `source_img` should be the image in the *source* space,
        i.e. the space you are transforming FROM. This keeps `limit_to_img`
        correct in both directions.
    """
    
    transformed_point = transform_point(intersection.point, original_x_start, original_y_start, to_global=to_global)
    line1_t = transform_line(intersection.line1, source_img, original_x_start, original_y_start, to_global)
    line2_t = transform_line(intersection.line2, source_img, original_x_start, original_y_start, to_global)
    return Intersection(line1_t, line2_t, transformed_point)