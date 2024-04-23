from enum import Enum
from typing import Union
from player import Player
from geometry.vector import Vector
from constants.game_constants import TILE_HEIGHT, TILE_WIDTH, FPS, LEVELS_PATH, N_LEVELS, HEIGHT, WIDTH, PIXEL_CORRECTION
from constants.player_constants import HITPOINTS
import pygame
import json


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

    def update_player_state(self, player: Player) -> bool:
        completed_level = False
        for x in HITPOINTS['x']:
            pos_x = player.position.x + x*player.width
            j_pos = int(pos_x // TILE_WIDTH)
            for y in HITPOINTS['y']:
                pos_y = player.position.y - y*player.height
                i_pos = int((HEIGHT - pos_y) // TILE_HEIGHT)
                
                # water kills you
                if self.map[i_pos][j_pos] == 9 or self.map[i_pos][j_pos] == 10:
                    player.alive = False
                elif self.map[i_pos][j_pos] == -2: # goal flag
                    completed_level = True

        return completed_level

    def simulate_move_point(self, position: Vector, velocity: Vector) -> tuple[bool, bool, Union[int, None], Union[int, None]]:
        # Function that determines if the player is going to hit something on the next frame, and
        # if so, updates if velocity and position, so it don't.
        # returns xkeep, ykeep, xnew, ynew
        next_pos = position + velocity * (1 / FPS)

        i_next = int((HEIGHT - next_pos.y) // TILE_HEIGHT)
        j_next = int(next_pos.x// TILE_WIDTH)
        
        keep_Xspeed, keep_Yspeed = True, True
        new_x, new_y = None, None
        
        if not self.is_valid(i_next, j_next) or self.map[i_next][j_next] >= 0:
            i_current = int((HEIGHT - position.y) // TILE_HEIGHT)
            j_current = int(position.x // TILE_WIDTH)
            
            updated = False
            if not self.is_valid(i_next, j_current) or self.map[i_next][j_current] >= 0:
                keep_Yspeed = False
                updated = True
            if not self.is_valid(i_current, j_next) or self.map[i_current][j_next] >= 0:
                keep_Xspeed = False
                updated = True

        if not keep_Xspeed:
            if velocity.x > 0:
                new_x = j_next * TILE_WIDTH - PIXEL_CORRECTION
            else:
                new_x = j_current * TILE_WIDTH + PIXEL_CORRECTION
        
        if not keep_Yspeed:
            if velocity.y < 0:
                new_y = HEIGHT - i_next * TILE_HEIGHT + PIXEL_CORRECTION
            else:
                new_y = HEIGHT - i_current * TILE_HEIGHT - PIXEL_CORRECTION
        return keep_Xspeed, keep_Yspeed, new_x, new_y

    def simulate_move_player(self, player: Player):
        keep_Xspeed, keep_Yspeed = True, True
        new_x, new_y = None, None
        can_jump = False
        for x in HITPOINTS['x']:
            for y in HITPOINTS['y']:
                if (not keep_Yspeed and not keep_Xspeed):
                    continue
                corner_position = player.position + Vector(x*player.width, -y*player.height)
                xkeep, ykeep, xnew, ynew = self.simulate_move_point(corner_position, player.velocity)
                keep_Xspeed = keep_Xspeed and xkeep
                keep_Yspeed = keep_Yspeed and ykeep

                if xnew is not None:
                    new_x = xnew - x * player.width
                if ynew is not None:
                    new_y = ynew + y * player.height
        if new_x is not None:
           player.position.x = new_x
        if new_y is not None:
           player.position.y = new_y
        
        if not keep_Xspeed:
            player.velocity.x = 0
        if not keep_Yspeed:
            if player.velocity.y < -0.1:
                player.jumping = False
            player.velocity.y = 0
    
    def draw(self, screen, anchor_point: tuple[float, float]):
        _, _, _, screen_height = screen.get_rect()
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == -2:
                    pygame.draw.rect(screen, (255, 0, 0),
                        (j*TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
                    continue
                if self.map[i][j] == -1:
                    continue
                pygame.draw.rect(screen, (0, 255, 0),
                    (j*TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

