from geometry.box import Box
from geometry.utils import get_points
from enum import Enum


class BlockType(Enum):
    EMPTY = -1
    GROUND = 0
    WALL = 1
    # add other types


class Block(Box):
    def __init__(self, x: float, y: float, width: float, height: float, grappble: bool = True):
        super().__init__(x, y, width, height)
        self.grappble = grappble