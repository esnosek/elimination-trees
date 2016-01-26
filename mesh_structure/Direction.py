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

class VectorDirection:
    
    def __init__(self):
        pass
        
    def get_vector_direction(self, v1, v2):
        if self.__is_direction_top(v1, v2):
            return Direction.top
        if self.__is_direction_right(v1, v2):
            return Direction.right
        if self.__is_direction_bottom(v1, v2):
            return Direction.bottom
        if self.__is_direction_left(v1, v2):
            return Direction.left

    def __is_direction_top(self, v1, v2):
        if v1.x == v2.x and v1.y < v2.y:
            return True
        return False

    def __is_direction_right(self, v1, v2):
        if v1.x < v2.x and v1.y == v2.y:
            return True
        return False

    def __is_direction_bottom(self, v1, v2):
        if v1.x == v2.x and v1.y > v2.y:
            return True
        return False

    def __is_direction_left(self, v1, v2):
        if v1.x > v2.x and v1.y == v2.y:
            return True
        return False
