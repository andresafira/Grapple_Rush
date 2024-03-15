from enum import Enum
from typing import Union

# pygame libraries management
import pygame
from pygame.tranfrom pygame.transform import scale, rotate
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
        self.state: GameState = GameState.MENU
        self.level: Union[None, int] = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.state == GameState.MENU:
                self.menu()
            elif self.state == GameState.GAME:
                self.game()
            elif self.state == GameState.OPTIONS:
                self.options()

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

