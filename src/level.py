from enum import Enum
from player import Player
from geometry.vector import Vector
from constants.game_constants import TILE_HEIGHT, TILE_WIDTH, FPS, LEVELS_PATH, N_LEVELS, HEIGHT, WIDTH
import pygame
import json


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    GROUND = 2
    # include other tile types


class Level:
    def __init__(self):
        self.map: list[list[Tile]] = [[]]

    def create(self, level_number: int):
        if level_number < 1 or level_number > N_LEVELS:
            raise Exception('Invalid level number: {}'.format(level_number))
        
        level_path = LEVELS_PATH + f'l{level_number}.json'
        
        with open(level_path, 'r') as file:
            self.map = json.load(file)
    
    def is_valid(self, i, j):
        if i < 0 or i >= len(self.map) or j < 0 or j >= len(self.map[0]):
            return False
        return True

    def simulate_move_corner(self, player, x_inc, y_inc) -> list[bool, bool]:
        next_pos = player.position + player.velocity * player.dt
        next_pos.x += x_inc*player.width
        next_pos.y -= y_inc*player.height

        i_next = int((HEIGHT - next_pos.y) // TILE_HEIGHT)
        j_next = int(next_pos.x // TILE_WIDTH)
        
        ans = [True, True]

        if not self.is_valid(i_next, j_next) or self.map[i_next][j_next] != 0:
            i_current = int((HEIGHT - player.position.y + y_inc*player.height) // TILE_HEIGHT)
            j_current = int((player.position.x + x_inc*player.width) // TILE_WIDTH)
            updated = False
            if not self.is_valid(i_next, j_current) or self.map[i_next][j_current] != 0:
                ans[1] = False
                updated = True
            if not self.is_valid(i_current, j_next) or self.map[i_current][j_next] != 0:
                ans[0] = False
                updated = True
            if not updated:
                ans = [False, False]
        return ans

    def simulate_move(self, player: Player):
        keep_speed = [True, True]
        for x in (0, 1):
            for y in (0, 1):
                temp = self.simulate_move_corner(player, x, y)
                keep_speed = [keep_speed[i] and temp[i] for i in range(2)]
        if not keep_speed[0]:
            player.velocity.x = 0
        if not keep_speed[1]:
            player.velocity.y = 0
            player.jumping = False
    
    def draw(self, screen, anchor_point: tuple[float, float]):
        _, _, _, screen_height = screen.get_rect()
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] != 1:
                    continue
                pygame.draw.rect(screen, (0, 255, 0),
                    (j*TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

