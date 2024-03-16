from enum import Enum
from typing import Union

# pygame libraries management
import pygame
from pygame.transform import scale, rotate
from pygame.image import load
from pygame.locals import *
from pygame import display

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60

class GameState(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    # add other states


class Engine:
    def __init__(self):
        pygame.init()
        self.state: GameState = GameState.MENU
        self.level: Union[None, int] = None

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            if self.state == GameState.MENU:
                self.menu()
            elif self.state == GameState.GAME:
                self.game()
            elif self.state == GameState.OPTIONS:
                self.options()

        pygame.quit()
        quit()

    def menu(self):
        # Stuff

        # if choose == play -> self.state = GameState.GAME
        # elif choose == options -> self.state = GameState.OPTIONS
        raise NotImplemented()

    def game(self):
        # Run the game
        raise NotImplemented()
    
    def options(self):
        # Stuff

        # if choose == menu -> self.state = GameState.Menu
        raise NotImplemented()

