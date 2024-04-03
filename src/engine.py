from enum import Enum
from typing import Union

from level import Level
from player import Player
from constants.game_constants import FPS, WIDTH, HEIGHT

# pygame libraries management
import pygame
from pygame.transform import scale, rotate
from pygame.image import load
from pygame.locals import *
from pygame import display


class GameState(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    # add other states


class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grappler Rush")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.state: GameState = GameState.GAME
        self.level: Union[None, Level] = Level()
        self.clock = pygame.time.Clock()
        
        self.level.create(level_number = 1)
        self.player: Union[None, Player] = Player(100, HEIGHT - 100, 20, 40)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[K_ESCAPE]:
                    running = False
                    break
            
            if self.state == GameState.MENU:
                self.menu()
            elif self.state == GameState.GAME:
                self.game()
            elif self.state == GameState.OPTIONS:
                self.options()
            else:
                raise Exception(f"Invalid Game State: {self.state}")

        pygame.quit()
    
    def draw_background(self):
        self.screen.fill((0, 0, 0))

    def draw_game(self):
        self.draw_background()
        self.level.draw(self.screen, (0, 0))
        self.player.draw(self.screen, (0, 0))
        # draw GH

        pygame.display.update()

    def menu(self):
        # Stuff

        # if choose == play -> self.state = GameState.GAME
        # elif choose == options -> self.state = GameState.OPTIONS
        raise NotImplemented()

    def game(self):
        keys = pygame.key.get_pressed()
        horizontal_movement = 'none'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            horizontal_movement = 'right'
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            horizontal_movement = 'left'
        else:
            horizontal_movement = 'none'

        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_c]:
            jump = True
        else:
            jump = False

        self.player.update_velocity(horizontal_movement, jump)
        self.level.simulate_move_player(self.player)
        self.player.move()

        self.draw_game()
    
    def options(self):
        # Stuff

        # if choose == menu -> self.state = GameState.Menu
        raise NotImplemented()

    
