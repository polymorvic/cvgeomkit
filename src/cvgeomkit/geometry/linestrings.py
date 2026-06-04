from typing import Iterator, Sequence, Self

from cvgeomkit.common import Hashable
from cvgeomkit.geometry.points import Point, transform_point
from cvgeomkit.geometry.segments import LineSegment


class LineString(Hashable):
    """
    Represents an ordered polyline made of two or more points.

    A LineString with 2 points contains 1 LineSegment.
    A LineString with N points contains N - 1 LineSegments.
    """

    __slots__ = ("_points",)

    def __init__(self, points: Sequence[Point]) -> None:
        if len(points) < 2:
            raise ValueError("LineString requires at least two points.")

        self._points = tuple(points)

        for p1, p2 in zip(self._points[:-1], self._points[1:]):
            if p1 == p2:
                raise ValueError("LineString cannot contain duplicated consecutive points.")

    def _key_(self) -> tuple[Point, ...]:
        return self._points

    @property
    def points(self) -> tuple[Point, ...]:
        return self._points

    @property
    def segments(self) -> tuple[LineSegment, ...]:
        return tuple(
            LineSegment(start, end)
            for start, end in zip(self._points[:-1], self._points[1:])
        )

    @property
    def start(self) -> Point:
        return self._points[0]

    @property
    def end(self) -> Point:
        return self._points[-1]

    @property
    def length(self) -> float:
        return sum(segment.length for segment in self.segments)

    @property
    def is_closed(self) -> bool:
        return self.start == self.end

    def to_tuples(self) -> tuple[tuple[int, int], ...]:
        return tuple(point.to_tuple() for point in self._points)

    def as_hough_segments(self) -> tuple[tuple[int, int, int, int], ...]:
        return tuple(segment.as_hough_segment() for segment in self.segments)

    def __iter__(self) -> Iterator[Point]:
        yield from self._points

    def __len__(self) -> int:
        return len(self._points)

    def __getitem__(self, index: int) -> Point:
        return self._points[index]

    def __repr__(self) -> str:
        segments = ", ".join(repr(segment) for segment in self.segments)
        return f"LineString([{segments}])"

    @classmethod
    def from_points(cls, points: Sequence[Point]) -> Self:
        return cls(points)

    @classmethod
    def from_tuples(cls, points: Sequence[tuple[int, int]]) -> Self:
        return cls([Point.from_iterable(point) for point in points])

    @classmethod
    def from_segments(cls, segments: Sequence[LineSegment]) -> Self:
        if not segments:
            raise ValueError("LineString requires at least one LineSegment.")

        points = [segments[0].start]
        for segment in segments:
            if points[-1] != segment.start:
                raise ValueError("Segments must be connected and ordered.")
            points.append(segment.end)

        return cls(points)


def transform_linestring(
    linestring: LineString,
    original_x_start: int,
    original_y_start: int,
    to_global: bool = True,
) -> LineString:
    points = [
        transform_point(
            point,
            original_x_start,
            original_y_start,
            to_global=to_global,
        )
        for point in linestring.points
    ]
    return LineString(points)