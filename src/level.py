from enum import Enum
import pygame
import os
from os.path import isfile, join
from constants.game_constants import WIDTH, HEIGHT


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

    def get_background(self, name):
        image = pygame.image.load(join("assets", "Background", name))
        _, _, width, height = image.get_rect()
        tiles = []

        for i in range(WIDTH // width + 1):
            for j in range(HEIGHT // height + 1):
                pos = (i * width, j * height)
                tiles.append(pos)

        return tiles, image

    def draw(self, window, background, bg_image):
        for tile in background:
            window.blit(bg_image, tile)

        pygame.display.update()