from constants.game_constants import WIDTH, HEIGHT, ROWS, COLS, TILE_WIDTH, TILE_HEIGHT, SIDE_MARGIN, LOWER_MARGIN, TILES_NUM, GREEN, RED, LEVELS_PATH, N_LEVELS
from button import Button
import pygame
import json


class Editor:
    def __init__(self, game_screen):
        self.level = 1
        self.text_font = pygame.font.SysFont('Futura', 30)
        self.initialized = -1
        self.tiles_list = []
        self.buttons_list = []
        self.map_info = []
        self.create_empty_map()
        self.current_tile = -1
        self.screen = game_screen
        self.mouse_pos = pygame.mouse.get_pos()

        self.save_button = Button(WIDTH // 2 + 60, HEIGHT + LOWER_MARGIN - 70, pygame.image.load(
            'buttons/save_btn.jpg').convert_alpha(), 0.25)
        self.load_button = Button(WIDTH // 2 + 260, HEIGHT + LOWER_MARGIN - 70, pygame.image.load(
            'buttons/load_btn.jpg').convert_alpha(), 0.25)

    def draw_text(self, text, color, x, y):
        image = self.text_font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def draw_grid(self):
        for col_num in range(COLS + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (col_num * TILE_WIDTH, 0), (col_num * TILE_WIDTH, HEIGHT))

        for row_num in range(ROWS + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, row_num * TILE_HEIGHT), (WIDTH, row_num * TILE_HEIGHT))

    def create_empty_map(self):
        for row in range(ROWS):
            row_empty = [-1] * COLS
            self.map_info.append(row_empty)

        for tile in range(0, COLS):
            self.map_info[ROWS - 1][tile] = 0

    def save_map(self):
        level_path = LEVELS_PATH + f'l{self.level}.json'

        with open(level_path, 'w') as file:
            json.dump(self.map_info, file)

    def load_map(self):
        self.map_info = []

        level_path = LEVELS_PATH + f'l{self.level}.json'

        with open(level_path, 'r') as file:
            self.map_info = json.load(file)

    def user_input(self):
        self.mouse_pos = pygame.mouse.get_pos()
        column_number = self.mouse_pos[0] // TILE_WIDTH
        row_number = self.mouse_pos[1] // TILE_HEIGHT

        if self.mouse_pos[0] < WIDTH and self.mouse_pos[1] < HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if self.map_info[row_number][column_number] != self.current_tile:
                    self.map_info[row_number][column_number] = self.current_tile

            if pygame.mouse.get_pressed()[2] == 1:
                self.map_info[row_number][column_number] = -1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.level += 1
                if event.key == pygame.K_DOWN and self.level > 1:
                    self.level -= 1

    def draw_map(self):
        for row_number, row in enumerate(self.map_info):
            for index, tile in enumerate(row):
                if tile != -1:
                    self.screen.blit(self.tiles_list[tile], (index * TILE_WIDTH, row_number * TILE_HEIGHT))

    def draw_tile_panel(self):
        if len(self.tiles_list) == 0:
            for tile_number in range(TILES_NUM):
                img = pygame.image.load(f'tiles/{tile_number}.png')
                img = pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT))
                self.tiles_list.append(img)

            button_col = 0
            button_row = 0
            for i in range(TILES_NUM):
                tile_button = Button(WIDTH + (75 * button_col) + 50, 75 * button_row + 50, self.tiles_list[i], 1)
                self.buttons_list.append(tile_button)
                button_col += 1

                if button_col == 3:
                    button_row += 1
                    button_col = 0

        pygame.draw.rect(self.screen, GREEN, (WIDTH, 0, SIDE_MARGIN, HEIGHT))

        if self.save_button.draw(self.screen):
            self.save_map()
        if self.load_button.draw(self.screen):
            self.load_map()

        for button_count, button in enumerate(self.buttons_list):
            if button.draw(self.screen):
                self.current_tile = button_count

        if self.current_tile != -1:
            pygame.draw.rect(self.screen, RED, self.buttons_list[self.current_tile].rect, 3)

