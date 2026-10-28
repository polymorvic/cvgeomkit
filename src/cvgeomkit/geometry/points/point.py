from typing import Iterator, Self

import numpy as np

from cvgeomkit.common import Hashable
from cvgeomkit.types import Numeric



class Point[T: (Numeric, Numeric)](Hashable):
    """Immutable 2D point represented as a generic point with two numbers."""

    __slots__ = ("_x", "_y")

    def __init__(self, x: T, y: T) -> None:
        """
        Create a new Point instance from X and Y coordinates.

        Args:
            x (T): The X coordinate (int or float).
            y (T): The Y coordinate (int or float).
        """
        object.__setattr__(self, "_x", x)
        object.__setattr__(self, "_y", y)

    def __setattr__(self, name: str, value: object) -> None:
        """Prevent modification after initialization."""
        raise AttributeError(f"'Point' object attribute '{name}' is read-only")

    def _key_(self) -> tuple[T, T]:
        """Return the key for hashing and equality comparison."""
        return (self._x, self._y)

    @classmethod
    def from_xy(cls, x: T, y: T) -> Self:
        """
        Create a Point from separate X and Y values.

        Args:
            x (T): The X coordinate (int or float).
            y (T): The Y coordinate (int or float).

        Returns:
            Point[T]: A new immutable Point instance.
        """
        return cls(x, y)

    @classmethod
    def from_iterable(cls, iterable: tuple[T, T] | list[T, T]) -> Self:
        """
        Create a Point from an iterable of exactly two elements.

        Args:
            iterable: An iterable containing exactly two numeric elements.

        Returns:
            Point[T]: A new immutable Point instance.

        Raises:
            ValueError: If the iterable does not contain exactly two elements.
        """
        values = tuple(iterable)
        if len(values) != 2:
            raise ValueError(f"Expected iterable of length 2, got {len(values)}")
        return cls(values[0], values[1])

    @property
    def x(self) -> T:
        """Get the X coordinate of the point."""
        return self._x

    @property
    def y(self) -> T:
        """Get the Y coordinate of the point."""
        return self._y

    def distance(self, another_point: Self) -> float:
        """Calculate Euclidean distance to another point."""
        return np.linalg.norm(
            np.array([self.x, self.y]) - np.array([another_point.x, another_point.y])
        )

    def is_in_area(self, p1: Self, p2: Self) -> bool:
        return p1.x < self.x < p2.x and p1.y < self.y < p2.y

    def __getitem__(self, index: int) -> T:
        """Allow indexing like a tuple."""
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise IndexError("Point index out of range")

    def __iter__(self) -> Iterator[float]:
        """Allow unpacking like a tuple."""
        yield self._x
        yield self._y

    def __len__(self) -> int:
        """Return length (always 2)."""
        return 2

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Point({self._x}, {self._y})"

    def __str__(self) -> str:
        """Return string representation."""
        return f"({self._x}, {self._y})"

    @property
    def as_int(self) -> Self:
        return Point(int(self.x), int(self.y))

    @property
    def as_tuple(self) -> tuple[T, T]:
        """
        Convert the Point to a tuple (x, y).

        Returns:
            tuple[T, T]: A tuple containing the X and Y coordinates.
        """
        return (self._x, self._y)


    def __add__(self, another: "Point | tuple | list | float | int") -> "Point":
        if not isinstance(another, (Point, tuple, list, float, int)):
            raise AttributeError('only numeric scalars or Point or iterables supported')
        
        if isinstance(another, (tuple, list)):
            another = Point.from_iterable(another)

        if isinstance(another, (float, int)):
            another = Point(another, another)

        return Point(self.x + another.x, self.y + another.y)

    def __radd__(self, another):
        return self + another

    def __mul__(self, scalar: int | float) -> Self:
        if not isinstance(scalar, (float, int)):
            raise AttributeError('Only numeric types supported')
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int | float) -> Self: # 5 * p1
        return self * scalar

    def __sub__(self, another: "Point | tuple | list | float | int") -> "Point":
        return self + (-another)
    
    def __neg__(self) -> Self:
        return self * -1

    def __rsub__(self, another) -> Self:
        return another + (-self)

    def __truediv__(self, scalar: int | float):
        if not isinstance(scalar, (float, int)):
            raise AttributeError('Only numeric types supported')

        if scalar == 0:
            raise ValueError('Only non-zero values supported')
        
        return Point(self.x / scalar, self.y / scalar)

    def __rtruediv__(self, scalar: float | int) -> Self:
        if not isinstance(scalar, (float, int)):
            raise AttributeError('Only numeric types supported')
        
        if self.x == 0 or self.y == 0:
            raise ValueError("Both x and y should be non-zero")

        return Point(scalar / self.x, scalar / self.y)