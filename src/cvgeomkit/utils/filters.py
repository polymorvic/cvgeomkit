from cvgeomkit.geometry.lines import Line


def filter_horizontal_lines(
    lines: list[Line],
    slope_thresh: float = 0.02,
    horizontal: bool = True,
) -> list[Line] | None:

    if horizontal:
        filtered = [
            line
            for line in lines
            if line.slope is not None and abs(line.slope) < slope_thresh
        ]
    else:
        filtered = [
            line
            for line in lines
            if line.slope is not None and abs(line.slope) > slope_thresh
        ]

    return filtered if filtered else None


def filter_vertical_lines(
    lines: list[Line],
    theta_thresh: float = 1.0
) -> list[Line] | None:
    lines = [line for line in lines if abs(line.theta - 90) < theta_thresh]
    return lines if lines else None