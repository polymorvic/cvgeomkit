import numpy as np

from cvgeomkit.geometry.options import LineSelection
from cvgeomkit.types import Numeric
from cvgeomkit.geometry.lines.line import Line


class LineGroup(Line):
    """
    A group of Line objects that are approximately aligned, represented as a single approximated line.

    The approximation is based on the median slope/intercept (for non-vertical lines)
    or median x-value (for vertical lines).
    """

    def __init__(self, lines: list[Line] = None) -> None:
        self.lines = lines or []

        if not self.lines:
            self.slope = self.intercept = self.xv = None
        else:
            self._calculate_line_approximation()

    def __repr__(self) -> str:
        """Return a string representation of the approximated line equation."""
        if not self.lines:
            return "LineGroup(empty)"

        if self.xv is not None:
            return f"LineGroup: x = {self.xv:.2f} (from {len(self.lines)} lines)"
        else:
            return f"LineGroup: y = {self.slope:.2f} * x + {self.intercept:.2f} (from {len(self.lines)} lines)"

    def process_line(
        self, line: Line, thresh_theta: Numeric, thresh_intercept: Numeric
    ) -> bool:
        """
        Try to add a Line to the group if it is similar enough to the reference line.

        Args:
            line (Line): The line to evaluate and possibly add.
            thresh_theta (float | int): Angular threshold for similarity in orientation.
            thresh_intercept (float | int): Threshold for similarity in intercept (used for non-vertical lines).

        Returns:
            bool: True if the line was added to the group, False otherwise.
        """
        ref = self.lines[0]
        found = False

        if abs(ref.theta - line.theta) < thresh_theta:
            if ref.xv is None and line.xv is None:
                if abs(ref.intercept - line.intercept) < thresh_intercept:
                    found = True

            if ref.xv is not None or line.xv is not None:
                found = True

            if found:
                self.lines.append(line)
                self._calculate_line_approximation()

        self.lines = sorted(self.lines, key=lambda line: -line.intercept)
        return found

    def get_line(self, selection: LineSelection) -> Line:
        return {
            LineSelection.MIN: self.lines[0],
            LineSelection.MAX: self.lines[-1],
        }[selection]

    def _calculate_line_approximation(self) -> None:
        """
        Calculate the approximated line for the group based on the median of included lines.

        - For vertical lines (with xv), median x is used.
        - For non-vertical lines, median slope and intercept are used.
        """
        vertical_lines = [line.xv for line in self.lines if line.xv is not None]

        if vertical_lines:
            self.xv = np.median(vertical_lines)
            self.slope, self.intercept = None, None

        else:
            self.xv = None
            self.slope = np.median([line.slope for line in self.lines])
            self.intercept = np.median([line.intercept for line in self.lines])


def group_lines(
    lines: list[Line], 
    thresh_theta: Numeric = 5, 
    thresh_intercept: Numeric = 10
) -> list[LineGroup]:
    """
    Group similar Line objects into LineGroups based on orientation and position thresholds.

    Args:
        lines (list[Line]): A list of Line objects to group.
        thresh_theta (Numeric): Maximum allowed angle difference between lines to be in the same group.
        thresh_intercept (Numeric): Maximum allowed intercept difference (for non-vertical lines).

    Returns:
        list[LineGroup]: A list of LineGroup objects representing grouped lines.
    """
    groups = []

    for line in lines:
        for group in groups:
            if group.process_line(line, thresh_theta, thresh_intercept):
                break
        else:
            groups.append(LineGroup([line]))

    return groups
