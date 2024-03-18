from geometry.vector import Vector
from constans.player_constants import *
from constants.game_constants import FPS
from typing import Union


class Player:
    def __init__(self, initial_pos: Vector):
        self.position: Vector = initial_pos
        self.velocity: Vector = Vector(0, 0)
        self.dt = 1 / FPS;
        self.alive: bool = True

        self.gh_position: Union[None, Vector] = None
        self.gh_attached: bool = False

        self.jumping: bool = False
        self.jump_pressing_ended: bool = False

    def update_velocity(self, horizontal_movement: str,
                              jump_pressed: bool):
        # Horizontal movement
        if horizontal_movement == 'left':
            target_speed = -MAX_HORIZONTAL_SPEED
        elif horizontal_movement == 'none':
            target_speed = 0
        elif horizontal_movement == 'right':
            target_speed = MAX_HORIZONTAL_SPEED

        acc_x = ACC_KP * (target_speed - self.velocity.x)
        self.velocity.x += acc_x * self.dt

        # Vertical movement
        acc_y = BASE_G_VALUE
        if jump_pressed:
            if not self.jumping:
                self.jumping = True
                self.jump_pressing_ended = False
                self.velocity.y = MAX_JUMP_SPEED
            if not self.jump_pressing_ended and self.velocity.y >= 0:
                # if the character is jumping for the first time and has positive velocity, the gravity becomes
                # smaller so that the player can control the jump height
                acc_y *= JUMP_G_CONTROL
        else:
            self.jump_pressing_ended = True

        if self.velocity.y < 0:
            # if the player is falling the gravity increases, in order to decrease fall time (enhancing control)
            acc_y *= FALL_G_MULTIPLIER

        self.velocity.y += acc_y * self.dt
    
    def move(self):
        self.position += self.velocity
