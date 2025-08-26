import pygame
import sys

class MazeBuilder:
    def __init__(self, rows=12, cols=8, cell_size=80):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size + 40
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🧩 Maze Builder")
        self.font = pygame.font.SysFont("Arial", 24)
        self.maze = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start_pos = None
        self.end_pos = None
        self.dragging = False
        self.draw_mode = 1
        self.clock = pygame.time.Clock()

    def get_cell(self, pos):
        x, y = pos
        return y // self.cell_size, x // self.cell_size

    def draw_grid(self, mouse_pos):
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * self.cell_size, row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if (row, col) == self.start_pos:
                    pygame.draw.rect(self.screen, (0, 200, 0), rect)
                elif (row, col) == self.end_pos:
                    pygame.draw.rect(self.screen, (200, 0, 0), rect)
                elif self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), rect)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (100, 149, 237), rect, 3)
                else:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect, 2)

    def draw_instructions(self):
        text = self.font.render("Drag to draw | S: Start | E: End | Enter: Save", True, (50, 50, 50))
        self.screen.blit(text, (10, self.height - 30))

    def build_maze(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((255, 255, 255))
            self.draw_grid(mouse_pos)
            self.draw_instructions()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.get_cell(pygame.mouse.get_pos())
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        self.dragging = True
                        self.draw_mode = 1 - self.maze[row][col]
                        self.maze[row][col] = self.draw_mode

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False

                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    row, col = self.get_cell(pygame.mouse.get_pos())
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        self.maze[row][col] = self.draw_mode

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        row, col = self.get_cell(pygame.mouse.get_pos())
                        if 0 <= row < self.rows and 0 <= col < self.cols:
                            self.start_pos = (row, col)
                    elif event.key == pygame.K_e:
                        row, col = self.get_cell(pygame.mouse.get_pos())
                        if 0 <= row < self.rows and 0 <= col < self.cols:
                            self.end_pos = (row, col)
                    elif event.key == pygame.K_RETURN:
                        running = False

            self.clock.tick(60)

        pygame.quit()
        return self.maze, self.start_pos, self.end_pos