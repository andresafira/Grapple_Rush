from constants.game_constants import WIDTH, HEIGHT, ROWS, COLS, TILE_WIDTH, TILE_HEIGHT, SIDE_MARGIN, LOWER_MARGIN, TILES_NUM, GREEN, RED
from button import Button
import pygame


class Editor:
    def __init__(self, game_screen):
        self.tiles_list = []
        self.buttons_list = []
        self.clicked_tile = -1
        self.screen = game_screen

    def draw_grid(self):
        for col_num in range(COLS + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (col_num * TILE_WIDTH, 0), (col_num * TILE_WIDTH, HEIGHT))

        for row_num in range(ROWS + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, row_num * TILE_HEIGHT), (WIDTH, row_num * TILE_HEIGHT))

    def draw_tile_panel(self):
        if len(self.tiles_list) == 0:
            for tile_number in range(TILES_NUM):
                img = pygame.image.load(f'Tiles/{tile_number}.png')
                img = pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT))
                self.tiles_list.append(img)

        if len(self.buttons_list) == 0:
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

        for button_count, button in enumerate(self.buttons_list):
            if button.draw(self.screen):
                self.clicked_tile = button_count

        if self.clicked_tile != -1:
            pygame.draw.rect(self.screen, RED, self.buttons_list[self.clicked_tile].rect, 3)

