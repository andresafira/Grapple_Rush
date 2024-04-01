from geometry.vector import Vector
from constants.player_constants import *
from constants.game_constants import FPS
from typing import Union
from math import fabs, sqrt
import pygame


class Player:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position: Vector = Vector(x, y)
        self.velocity: Vector = Vector(0, 0)
        self.dt = 1 / FPS;
        self.alive: bool = True
        self.height = height
        self.width = width

        self.gh_position: Vector = Vector(x + width/1.5, y - height / 2)
        self.gh_velocity: Vector = Vector(0, 0)

        # reduce number of boolean
        self.gh_attached: bool = False
        self.gh_approaching: bool = False
        self.gh_holstered: bool = True
        self.gh_threw: bool = False
        self.gh_surface = pygame.Surface((15, 5))

        self.jumping: bool = True
        self.jump_pressing_ended: bool = False

    def update_gh_aim(self, screen):
        _, _, _, screen_height = screen.get_rect()

        if self.gh_threw:
            self.gh_holstered = False
            self.gh_approaching = False
            mouse_position : Vector = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            mouse_dist = sqrt((mouse_position.x - self.gh_position.x) ** 2 + (mouse_position.y - (screen_height - self.gh_position.y)) ** 2)
            self.gh_velocity.x = GRAPPLING_HOOK_SPEED * (mouse_position.x - self.gh_position.x) / mouse_dist
            self.gh_velocity.y = -GRAPPLING_HOOK_SPEED * (mouse_position.y - (screen_height - self.gh_position.y)) / mouse_dist

        self.gh_threw = False

        gh_distance = sqrt((self.position.x - self.gh_position.x) ** 2 + (self.position.y - self.gh_position.y) ** 2)

        if gh_distance > GH_MAX_LENGTH:
            self.gh_approaching = True
            self.gh_velocity.x = -self.gh_velocity.x
            self.gh_velocity.y = -self.gh_velocity.y

        if self.gh_approaching and gh_distance < GH_MIN_LENGTH:
            self.gh_holstered = True
            self.gh_attached = False
            self.gh_velocity.x = 0
            self.gh_velocity.y = 0

        if self.gh_attached:
            self.gh_approaching = True
            gh_dist = sqrt((self.position.x - self.gh_position.x) ** 2 + (self.position.y - self.gh_position.y) ** 2)
            self.velocity.x = -GRAPPLING_HOOK_SPEED * (self.position.x - self.gh_position.x) / gh_dist
            self.velocity.y = -GRAPPLING_HOOK_SPEED * (self.position.y - self.gh_position.y) / gh_dist
            self.gh_velocity.x = 0
            self.gh_velocity.y = 0

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
            if not self.jumping and fabs(self.velocity.y) < 50:
                self.jumping = True
                self.jump_pressing_ended = False
                self.velocity.y = MAX_JUMP_SPEED
            if not self.jump_pressing_ended and self.velocity.y > 1:
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
        if self.gh_attached:
            self.position = self.position + self.velocity * self.dt
        else:
            self.position = self.position + self.velocity * self.dt
            if self.gh_holstered:
                self.gh_position.x = self.position.x
                self.gh_position.y = self.position.y
            self.gh_position = self.gh_position + self.gh_velocity * self.dt + self.velocity * self.dt

    def draw(self, screen, anchor_point):
        _, _, _, screen_height = screen.get_rect()
        pygame.draw.rect(screen, (255, 0, 0),
                (self.position.x, screen_height - self.position.y, self.width, self.height))

        pygame.draw.rect(screen, (0, 0, 255), (self.gh_position.x, screen_height - self.gh_position.y, 15, 5))
