from enum import Enum
from typing import Union

from level import Level
from player import Player
from editor import Editor
from constants.game_constants import FPS, WIDTH, HEIGHT, SIDE_MARGIN, LOWER_MARGIN, GREEN, WHITE, BLACK, N_LEVELS
from constants.player_constants import PLAYER_WIDTH, PLAYER_HEIGHT

# pygame libraries management
import pygame
from pygame.transform import scale, rotate
from pygame.image import load
from pygame.locals import *
from pygame import display

from button import Button

class GameState(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    EDITOR = 3
    END = 4
    # add other states


class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grapple Rush")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.resized = False

        self.state: GameState = GameState.MENU
        self.level_number: int = 1
        self.level: Union[None, Level] = Level()
        self.level_editor = Editor(self.screen)
        self.clock = pygame.time.Clock()
        self.level.create(level_number = self.level_number)
        self.player: Union[None, Player] = Player(20, 130, PLAYER_WIDTH, PLAYER_HEIGHT)

        self.pine1_img = pygame.image.load('background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('background/mountain2.png').convert_alpha()
        self.sky_cloud_img = pygame.image.load('background/sky_cloud.png').convert_alpha()
        self.sky_img = pygame.image.load('background/sky_2.png').convert_alpha()

        self.menu_img = pygame.image.load('background/menu_background.png').convert_alpha()
        self.menu_img = scale(self.menu_img, (WIDTH, HEIGHT))

        self.end_img = scale(pygame.image.load('background/thend.png').convert_alpha(), (WIDTH, HEIGHT))

        self.text_font = pygame.font.SysFont('Futura', 30)

        self.play_button = Button(WIDTH // 2 - 30, HEIGHT - 200, pygame.image.load(
            'buttons/play_btn.jpg').convert_alpha(), 0.3)
        self.editor_button = Button(WIDTH // 2 - 30, HEIGHT - 100, pygame.image.load(
            'buttons/edit_level_btn.jpg').convert_alpha(), 0.3)
        self.menu_button = Button(WIDTH - 150, HEIGHT - 100, pygame.image.load(
            'buttons/menu_btn.jpg').convert_alpha(), 0.3)
        self.editor_menu_button = Button(WIDTH // 2 + 460, HEIGHT + LOWER_MARGIN - 70, pygame.image.load(
            'buttons/menu_btn.jpg').convert_alpha(), 0.25)

        self.elapsed_time: float = 0.0

        self.apply_music()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            if self.state == GameState.MENU:
                self.menu()
            elif self.state == GameState.GAME:
                self.game()
            elif self.state == GameState.EDITOR:
                self.editor()
            elif self.state == GameState.END:
                self.end()
            else:
                raise Exception(f"Invalid Game State: {self.state}")

        pygame.quit()

    def draw_background(self):
        self.screen.fill(GREEN)
        width = self.sky_img.get_width()
        for x in range(3):
            self.screen.blit(self.sky_img, ((x * width),
                            HEIGHT - 3*self.sky_img.get_height()))
            self.screen.blit(self.sky_img, ((x * width),
                            HEIGHT - 2 * self.sky_img.get_height() - 30))
            self.screen.blit(self.sky_cloud_img, ((x * width), 0))
            self.screen.blit(self.mountain_img, ((x * width),
                            HEIGHT - self.mountain_img.get_height() - 180))
            self.screen.blit(self.pine1_img, ((x * width),
                            HEIGHT - self.pine1_img.get_height() - 100))
            self.screen.blit(self.pine2_img, ((x * width),
                            HEIGHT - self.pine2_img.get_height()))

    def draw_game(self):
        self.draw_background()
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        # draw GH

    def apply_music(self):
        if self.state == GameState.MENU:
            pygame.mixer.music.load('ost/CPOR_BRASIL.mp3')
        elif self.state == GameState.GAME:
            pygame.mixer.music.load('ost/apotechary.mp3')
        elif self.state == GameState.EDITOR:
            pygame.mixer.music.load('ost/wave.mp3')
        elif self.state == GameState.END:
            pygame.mixer.music.load('ost/sunshine.mp3')
        else:
            raise Exception('Invalid game state')

        pygame.mixer.music.play(-1)

    def menu(self):
        self.screen.blit(self.menu_img, (0, 0))

        if self.play_button.draw(self.screen):
            self.level_number = 1
            pygame.time.wait(200)

            self.elapsed_time = self.clock.get_time()
            self.elapsed_time = 0

            self.state = GameState.GAME
            self.apply_music()
        if self.editor_button.draw(self.screen):
            self.state = GameState.EDITOR
            self.apply_music()

        pygame.display.update()

    def restart_player(self):
        self.player = Player(20, 130, PLAYER_WIDTH, PLAYER_HEIGHT)

    def game(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.state = GameState.MENU
            self.apply_music()

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

        if pygame.mouse.get_pressed()[0]:
            self.player.mouse_click = True
        else:
            self.player.mouse_click = False

        if keys[pygame.K_SPACE] and self.player.gh_attached:
           self.player.space_key = True

        self.player.update_velocity(horizontal_movement, jump)
        self.player.update_gh_aim(self.screen) # change function name and divide it in smaller functions
        self.level.simulate_move_player(self.player)
        self.level.simulate_move_gh(self.player)
        self.player.move()

        level_finished = self.level.update_player_state(self.player)
        self.draw_game()
        self.draw_timer()
        pygame.display.update()
        if not self.player.alive:
            self.restart_player()

        if level_finished:
            self.restart_player()
            self.level_number += 1
            if self.level_number > N_LEVELS:
                self.state = GameState.END
                self.apply_music()
            else:
                self.level.create(self.level_number)

    def draw_timer(self):
        self.elapsed_time += self.clock.get_time()

        current_time_s = int(self.elapsed_time / 1000)
        minutes: int = int(current_time_s // 60)
        seconds: int = int(current_time_s - minutes * 60)
        timer: str = '{:0>2}:{:0>2}'.format(minutes, seconds)

        text_img = self.text_font.render(timer, True, BLACK)
        self.screen.blit(text_img, (10, 10))

    def editor(self):
        if not self.resized:
            self.screen = pygame.display.set_mode((WIDTH + SIDE_MARGIN, HEIGHT + LOWER_MARGIN))
            self.resized = True
        pygame.display.flip()

        self.draw_background()
        self.level_editor.draw_grid()
        self.level_editor.draw_tile_panel()
        self.level_editor.draw_map()
        self.level_editor.draw_text(f'User level: {self.level_editor.level}', WHITE, 10, HEIGHT + LOWER_MARGIN - 90)
        self.level_editor.draw_text('Press UP or DOWN to change level. Right-click to delete a block', WHITE, 10, HEIGHT + LOWER_MARGIN - 60)
        self.level_editor.user_input()
        if self.editor_menu_button.draw(self.screen):
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.resized = False
            self.state = GameState.MENU
            self.apply_music()

        pygame.display.update()

    def end(self):
        self.screen.blit(self.end_img, (0, 0))        
        if self.menu_button.draw(self.screen):
            self.state = GameState.MENU
            self.apply_music()

        pygame.display.update()
