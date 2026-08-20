class NotEnoughLineSegmentsFound(Exception):
    def __init__(self, message="Not enough line segments found to interpolate"):
        super().__init__(message)