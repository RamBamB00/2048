import pygame
import random

class Tile:
    def __init__(self, value=0):
        self.value = value

    def draw(self, screen, x, y, tile_size):
        colors = {
            0: (205, 192, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
            4096: (60, 58, 50),
            8192: (60, 58, 50),
        }
        color = colors.get(self.value, (0, 0, 0))
        pygame.draw.rect(screen, color, (x, y, tile_size, tile_size), 0)
        if self.value != 0:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.value), True, (119, 110, 101))
            screen.blit(text, (x + tile_size/2 - text.get_width()/2, y + tile_size/2 - text.get_height()/2))

class Game2048:
    def __init__(self, screen, size, starting_tiles):
        self.screen = screen
        self.size = size
        self.grid = [[Tile() for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.high_score = 0
        self.add_starting_tiles(starting_tiles)

    def add_starting_tiles(self, num_tiles):
        for _ in range(num_tiles):
            self.add_tile()

    def add_tile(self):
        empty_tiles = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j].value == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j].value = 2 if random.random() < 0.9 else 4

    def draw(self):
        tile_size = 80
        margin = 10
        for row in range(self.size):
            for col in range(self.size):
                x = col * (tile_size + margin)
                y = row * (tile_size + margin)
                self.grid[row][col].draw(self.screen, x, y, tile_size)
        self.draw_score()

    def draw_score(self):
        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        text = font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
        self.screen.blit(text, (10, 30))

    def merge(self, direction):
        moved = False

        if direction == pygame.K_UP:
            for col in range(self.size):
                for row in range(1, self.size):
                    if self.grid[row][col].value != 0:
                        current_row = row
                        while current_row > 0 and self.grid[current_row - 1][col].value == 0:
                            self.grid[current_row - 1][col].value = self.grid[current_row][col].value
                            self.grid[current_row][col].value = 0
                            current_row -= 1
                            moved = True
                        if current_row > 0 and self.grid[current_row - 1][col].value == self.grid[current_row][col].value:
                            self.grid[current_row - 1][col].value *= 2
                            self.grid[current_row][col].value = 0
                            self.score += self.grid[current_row - 1][col].value
                            moved = True

        elif direction == pygame.K_DOWN:
            for col in range(self.size):
                for row in range(self.size - 2, -1, -1):
                    if self.grid[row][col].value != 0:
                        current_row = row
                        while current_row < self.size - 1 and self.grid[current_row + 1][col].value == 0:
                            self.grid[current_row + 1][col].value = self.grid[current_row][col].value
                            self.grid[current_row][col].value = 0
                            current_row += 1
                            moved = True
                        if current_row < self.size - 1 and self.grid[current_row + 1][col].value == self.grid[current_row][col].value:
                            self.grid[current_row + 1][col].value *= 2
                            self.grid[current_row][col].value = 0
                            self.score += self.grid[current_row + 1][col].value
                            moved = True

        elif direction == pygame.K_LEFT:
            for row in range(self.size):
                for col in range(1, self.size):
                    if self.grid[row][col].value != 0:
                        current_col = col
                        while current_col > 0 and self.grid[row][current_col - 1].value == 0:
                            self.grid[row][current_col - 1].value = self.grid[row][current_col].value
                            self.grid[row][current_col].value = 0
                            current_col -= 1
                            moved = True
                        if current_col > 0 and self.grid[row][current_col - 1].value == self.grid[row][current_col].value:
                            self.grid[row][current_col - 1].value *= 2
                            self.grid[row][current_col].value = 0
                            self.score += self.grid[row][current_col - 1].value
                            moved = True

        elif direction == pygame.K_RIGHT:
            for row in range(self.size):
                for col in range(self.size - 2, -1, -1):
                    if self.grid[row][col].value != 0:
                        current_col = col
                        while current_col < self.size - 1 and self.grid[row][current_col + 1].value == 0:
                            self.grid[row][current_col + 1].value = self.grid[row][current_col].value
                            self.grid[row][current_col].value = 0
                            current_col += 1
                            moved = True
                        if current_col < self.size - 1 and self.grid[row][current_col + 1].value == self.grid[row][current_col].value:
                            self.grid[row][current_col + 1].value *= 2
                            self.grid[row][current_col].value = 0
                            self.score += self.grid[row][current_col + 1].value
                            moved = True

        if moved:
            self.add_tile()
            if self.score > self.high_score:
                self.high_score = self.score

        return moved


def main():
    pygame.init()
    resolution = 360
    screen = pygame.display.set_mode((resolution, resolution))
    pygame.display.set_caption("2048")

    clock = pygame.time.Clock()
    running = True
    pygame.mixer.music.load('background_music.wav')
    pygame.mixer.music.play(-1)

    game_over_image = pygame.image.load("game_over.png")

    while running:
        screen.fill((187, 173, 160))
        font = pygame.font.Font(None, 36)

        easy_text = font.render("Hard (4x4)", True, (0, 0, 0))
        medium_text = font.render("Medium (6x6)", True, (0, 0, 0))
        hard_text = font.render("Easy (8x8)", True, (0, 0, 0))

        easy_rect = easy_text.get_rect(center=(resolution//2, 3*resolution//4))
        medium_rect = medium_text.get_rect(center=(resolution//2, resolution//2))
        hard_rect = hard_text.get_rect(center=(resolution//2, resolution//4))

        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    size = 4
                    resolution = 360
                    running = False
                elif medium_rect.collidepoint(event.pos):
                    size = 6
                    resolution = 540
                    running = False
                elif hard_rect.collidepoint(event.pos):
                    size = 8
                    resolution = 720
                    running = False

    screen = pygame.display.set_mode((resolution, resolution))
    game = Game2048(screen, size, 2)

    while True:
        screen.fill((187, 173, 160))
        game.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    game.merge(event.key)

        game_over = True
        for row in game.grid:
            for tile in row:
                if tile.value == 0:
                    game_over = False
                    break
            if not game_over:
                break
        if game_over:
            screen.blit(game_over_image, (resolution//2 - game_over_image.get_width()//2, resolution//2 - game_over_image.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            return

        clock.tick(60)

if __name__ == "__main__":
    main()
