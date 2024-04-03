from enum import Enum
from typing import Union

from level import Level
from player import Player
from constants.game_constants import FPS, WIDTH, HEIGHT, ROWS, COLS, TILE_WIDTH, TILE_HEIGHT, SIDE_MARGIN, LOWER_MARGIN

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
    EDITOR = 3
    # add other states


class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grappler Rush")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.resized = False
        self.state: GameState = GameState.EDITOR
        self.level: Union[None, Level] = Level()
        self.clock = pygame.time.Clock()
        
        self.level.create(level_number = 1)
        self.player: Union[None, Player] = Player(100, HEIGHT - 100, 20, 40)

        self.pine1_img = pygame.image.load('Background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('Background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('Background/mountain2.png').convert_alpha()
        self.sky_cloud_img = pygame.image.load('Background/sky_cloud.png').convert_alpha()
        self.sky_img = pygame.image.load('Background/sky_2.png').convert_alpha()

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
            elif self.state == GameState.EDITOR:
                self.editor()
            else:
                raise Exception(f"Invalid Game State: {self.state}")

        pygame.quit()
    
    def draw_background(self):
        self.screen.fill((0, 0, 0))
        width = self.sky_img.get_width()
        for x in range(3):
            self.screen.blit(self.sky_img, ((x * width), HEIGHT - 3*self.sky_img.get_height()))
            self.screen.blit(self.sky_img, ((x * width), HEIGHT - 3 * self.sky_img.get_height() - 60))
            self.screen.blit(self.sky_cloud_img, ((x * width), 0))
            self.screen.blit(self.mountain_img, ((x * width), HEIGHT - self.mountain_img.get_height() - 400))
            self.screen.blit(self.pine1_img, ((x * width), HEIGHT - self.pine1_img.get_height() - 350))
            self.screen.blit(self.pine2_img, ((x * width), HEIGHT - self.pine2_img.get_height() - 300))

    def draw_game(self):
        self.draw_background()
        self.level.draw(self.screen, (0, 0))
        self.player.draw(self.screen, (0, 0))
        # draw GH

        pygame.display.update()

    def draw_grid(self):
        for col_num in range(COLS + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (col_num * TILE_WIDTH, 0), (col_num * TILE_WIDTH, HEIGHT))

        for row_num in range(ROWS + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, row_num * TILE_HEIGHT), (WIDTH, row_num * TILE_HEIGHT))

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
        self.level.simulate_move(self.player)
        self.player.move()

        self.draw_game()
    
    def options(self):
        # Stuff

        # if choose == menu -> self.state = GameState.Menu
        raise NotImplemented()

    def editor(self):
        if not self.resized:
            self.screen = pygame.display.set_mode((WIDTH + SIDE_MARGIN, HEIGHT + LOWER_MARGIN))
            self.resized = True
        pygame.display.flip()
        self.draw_background()
        self.draw_grid()

        pygame.display.update()
