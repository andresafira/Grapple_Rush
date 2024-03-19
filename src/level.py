from enum import Enum
from player import Player
from constants.game_constants import TILE_HEIGHT, TILE_WIDTH, FPS
import json


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    GROUND = 2
    # include other tile types


class Level:
    def __init__(self):
        self.map: list[list[Tile]] = [[]]

    def create_from(self, path: str):
        with open(path, 'rb') as file:
            self.map = json.load(file)
    
    def is_valid(self, i, j):
        if i < 0 or i >= len(self.map) or j < 0 or j >= len(self.map[0]):
            return False
        return True

    def simulate_move(self, player: Player):
        next_pos = player.position + player.velocity / FPS
        
        # Assuming the player is in a valid square, we only have to look for the direction
        # it is moving to determine if a collision is going to happen
        x_increment = 0
        if player.velocity.x > 0:
            x_increment = player.width

        y_increment = 0
        if player.velocity.y < 0:
            y_increment = -player.height

        i_next = int(next_pos.y + y_increment / TILE_HEIGHT)
        j_next = int(next_pos.x + x_increment / TILE_WIDTH)
        if not self.is_valid(i_next, j_next) or self.map[i_next][j_next] != Tile.EMPTY:
            i_current = int(player.position.y + x_increment / TILE_HEIGHT)
            j_current = int(player.position.x + y_increment / TILE_WIDTH)
            if i_next != i_current:
                player.velocity.y = 0
            if j_next != j_current:
                player.velocity.x = 0
            # If the player is with the GH attached and collide with something,
            # maybe we can detach it, or other action
