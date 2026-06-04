from typing import Iterator, Self, TYPE_CHECKING

import numpy as np

from cvgeomkit.common import Hashable
from cvgeomkit.geometry.points import Point, transform_point
from cvgeomkit.geometry.lines import Line

if TYPE_CHECKING:
    from .intersections import Intersection


class LineSegment(Hashable):
    """
    Represents a finite 2D line segment defined by two endpoints

    Unlike `Line`, which represents an infinite mathematical line,
    `LineSegment` represents only the bounded part between `start` and `end`
    """

    __slots__ = ("_start", "_end", "_line")

    def __init__(self, start: Point, end: Point) -> None:
        if start == end:
            raise ValueError("LineSegment requires two different points.")

        self._start = start
        self._end = end
        self._line = Line.from_points(start.to_tuple(), end.to_tuple())

    def _key_(self) -> tuple[Point, Point]:
        return self._start, self._end

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    @property
    def line(self) -> Line:
        return self._line

    @property
    def length(self) -> float:
        return self._start.distance(self._end)

    @property
    def theta(self) -> float:
        return self._line.theta

    @property
    def midpoint(self) -> Point:
        return Point(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
        )

    def to_tuple(self) -> tuple[Point, Point]:
        return self.start, self.end

    def as_hough_segment(self) -> tuple[int, int, int, int]:
        return (
            int(self.start.x),
            int(self.start.y),
            int(self.end.x),
            int(self.end.y),
        )

    def __iter__(self) -> Iterator[Point]:
        yield self.start
        yield self.end

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> Point:
        if index == 0:
            return self.start
        if index == 1:
            return self.end
        raise IndexError("LineSegment index out of range")


    def __repr__(self) -> str:
        if self.line.xv is not None:
            equation = f"x = {self.line.xv:.2f}"
        else:
            equation = f"y = {self.line.slope:.2f}x + {self.line.intercept:.2f}"

        return f'LineSegment(start={self.start}, end={self.end}, line={equation})'
    

    @classmethod
    def from_points(cls, start: Point, end: Point) -> Self:
        return cls(start, end)

    @classmethod
    def from_tuples(cls, start: tuple[int, int], end: tuple[int, int]) -> Self:
        return cls(Point.from_iterable(start), Point.from_iterable(end))

    @classmethod
    def from_hough_segment(cls, hough_segment: tuple[int, int, int, int]) -> Self:
        x1, y1, x2, y2 = hough_segment
        return cls(Point(x1, y1), Point(x2, y2))

    @classmethod
    def from_line_and_image(cls, line: Line, image: np.ndarray) -> Self:
        start, end = line.limit_to_img(image)
        return cls(start, end)


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