from geometry.vector import Vector
from constants.player_constants import *
from constants.game_constants import FPS
from typing import Union
from math import fabs
import pygame
from pygame.transform import scale, flip
from pygame.image import load
from pygame.locals import *
from enum import Enum


class SpriteState(Enum):
    IDLE = 0
    JUMPING = 1
    MIDAIR = 2
    FALLING = 3
    HOOKED = 4
    RUNNING = 5


class Player:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position: Vector = Vector(x, y)
        self.velocity: Vector = Vector(0, 0)
        self.dt = 1 / FPS;
        self.alive: bool = True
        self.height = height
        self.width = width

        self.gh_position: Union[None, Vector] = None
        self.gh_attached: bool = False

        self.jumping: bool = True
        self.jump_pressing_ended: bool = False

        # sprites
        idle_sprites: list = [scale(load(f'sprites/idle/idle{i}.png'), (width, height)) for i in range(12)]
        midair_sprites: list = [scale(load(f'sprites/jump/midair1.png'), (width, height))]
        falling_sprites: list = [scale(load('sprites/jump/midair3.png'), (width, height))]
        jumping_sprites: list = [scale(load('sprites/jump/midair0.png'), (width, height))]
        run_sprites: list = [scale(load(f'sprites/run/run{i}.png'), (width, height)) for i in range(8)]
        hooked_sprites: list = [scale(load(f'sprites/hook/hook{i}.png'), (width, height)) for i in range(6)]
        
        self.sprites: dict[SpriteState, list] = {SpriteState.IDLE: idle_sprites, SpriteState.RUNNING: run_sprites,
                        SpriteState.HOOKED: hooked_sprites, SpriteState.JUMPING: jumping_sprites, 
                        SpriteState.MIDAIR: midair_sprites, SpriteState.FALLING: falling_sprites}

        self.sprite_state: SpriteState = SpriteState.IDLE
        self.flip_sprite: bool = False
        self.sprite_count: int = 0
        self.frame_count: int = 0

    def change_sprite_state(self, new_state: SpriteState):
        if self.sprite_state == new_state:
            return
        self.sprite_state = new_state
        self.sprite_count = 0

    def update_velocity(self, horizontal_movement: str,
                              jump_pressed: bool):
        if self.velocity.abs() < 20:
            self.change_sprite_state(SpriteState.IDLE)

        # Horizontal movement
        if horizontal_movement == 'left':
            target_speed = -MAX_HORIZONTAL_SPEED
        elif horizontal_movement == 'none':
            target_speed = 0
        elif horizontal_movement == 'right':
            target_speed = MAX_HORIZONTAL_SPEED

        acc_x = ACC_KP * (target_speed - self.velocity.x)
        self.velocity.x += acc_x * self.dt
        if self.velocity.x > 20:
            self.change_sprite_state(SpriteState.RUNNING)
            self.flip_sprite = False
        elif self.velocity.x < -20:
            self.change_sprite_state(SpriteState.RUNNING)
            self.flip_sprite = True

        # Vertical movement
        acc_y = BASE_G_VALUE
        if self.jumping:
            self.change_sprite_state(SpriteState.MIDAIR)

        if jump_pressed:
            if not self.jumping and fabs(self.velocity.y) < 50:
                self.jumping = True
                self.jump_pressing_ended = False
                self.velocity.y = MAX_JUMP_SPEED

                self.change_sprite_state(SpriteState.JUMPING)
            if not self.jump_pressing_ended and self.velocity.y > 1:
                # if the character is jumping for the first time and has positive velocity, the gravity becomes
                # smaller so that the player can control the jump height
                acc_y *= JUMP_G_CONTROL
                self.change_sprite_state(SpriteState.JUMPING)
        else:
            self.jump_pressing_ended = True

        if self.velocity.y < -20:
            # if the player is falling the gravity increases, in order to decrease fall time (enhancing control)
            self.change_sprite_state(SpriteState.FALLING)
            acc_y *= FALL_G_MULTIPLIER

        self.velocity.y += acc_y * self.dt
    
    def move(self):
        self.position = self.position + self.velocity * self.dt

    def draw(self, screen):
        _, _, _, screen_height = screen.get_rect()

        frame_speed = 4
        self.frame_count += 1

        if self.frame_count == frame_speed:
            self.frame_count = 0
            self.sprite_count += 1
            if self.sprite_count >= len(self.sprites[self.sprite_state]):
                self.sprite_count = 0
        sprite = flip(self.sprites[self.sprite_state][self.sprite_count], flip_x = self.flip_sprite, flip_y = False)
        screen.blit(sprite, (self.position.x, screen_height - self.position.y, self.width, self.height))
