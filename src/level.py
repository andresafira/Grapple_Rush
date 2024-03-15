from enum import Enum


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    GROUND = 2
    # include other tile types


class Level:
    def __init__(self, height_in_tiles: int, width_in_tiles: int):
        self.map = [[Tile.EMPTY for _ in range(width_in_tiles)] for __ in range(height_in_tiles)]

    def create_from_txt(self, path: str):
        with open(path, 'r') as file:
            txt = file.read()

        # manage txt and then remove the following line
        raise NotImplemented()
    
    def 

