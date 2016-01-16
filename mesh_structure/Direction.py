from enum import Enum


class Direction(Enum):
    top = 0
    right = 1
    bottom = 2
    left = 3

    def get_oposite_direction(self):
        if self == Direction.bottom:
            return Direction.top
        elif self == Direction.left:
            return Direction.right
        elif self == Direction.top:
            return Direction.bottom
        else:
            return Direction.left
