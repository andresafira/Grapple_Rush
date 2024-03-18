from geometry.vector import Vector
from typing import Union
from player_constants import *
from enum import Enum


class HorizontalMovement(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Player:
    def __init__(self, initial_pos: Vector):
        self.position: Vector = initial_pos
        self.velocity: Vector = Vector(0, 0)
        self.alive: bool = True

        self.gh_position: Union[None, Vector] = None
        self.gh_attached: bool = False

        self.jumping: bool = False
        self.jump_pressing_ended: bool = False

    def move_without_gh(self, horizontal_movement: HorizontalMovement,
                              jump_pressed: bool):
        self.position += self.velocity * 0.01 # ADD *dt when we have a game_constants.py
        
        # HERE IS THE DIFFICULT PART, WE HAVE TO ANALYZE COLLISIONS IN ORDER TO CHECK IF THE JUMP ENDED OR IN ORDER TO CLIP THE POSITION TO STOP THE MOVEMENT

        # Horizontal movement
        if horizontal_movement == HorizontalMovement.LEFT:
            target_speed = -MAX_HORIZONTAL_SPEED
        elif horizontal_movement == HorizontalMovement.NONE:
            target_speed = 0
        elif horizontal_movement == HorizontalMovement.RIGHT:
            target_speed = MAX_HORIZONTAL_SPEED

        acc_x = ACC_KP * (target_speed - self.velocity.x)
        self.velocity.x += acc_x * 0.01 # ADD *dt when we have a game_constants.py

        # Vertical movement
        acc_y = BASE_G_VALUE
        if jump_pressed:
            if not self.jumping:
                self.jumping = True
                self.jump_pressing_ended = False
                self.velocity.y = MAX_JUMP_SPEED
            if not self.jump_pressing_ended and self.velocity.y >= 0:
                acc_y *= JUMP_G_CONTROL
        else:
            self.jump_pressing_ended = True

        if self.velocity.y < 0:
            acc_y *= FALL_G_MULTIPLIER

        self.velocity.y += acc_y * 0.01 # ADD *dt when we have a game_constants.py


