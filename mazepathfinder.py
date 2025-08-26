from mazebuilder import *
import pygame

path = {}
parent = {}
alreadysearched = {}
stack = []

builder = MazeBuilder()
maze_array, start, end = builder.build_maze()
checkstart = start

def display_explored_maze(matrix, explored, start, end, cell_size=80):
    pygame.init()
    rows = len(matrix)
    cols = len(matrix[0])
    width = cols * cell_size
    height = rows * cell_size + 40

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Explorer")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))

        for row in range(rows):
            for col in range(cols):
                x, y = col * cell_size, row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                coord = (row, col)

                if coord == start or coord == end:
                    pygame.draw.rect(screen, (200, 0, 0), rect)
                elif matrix[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                elif coord in path:
                    pygame.draw.rect(screen, (255, 255, 0), rect)
                elif coord in explored:
                    pygame.draw.rect(screen, (173, 216, 230), rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)

                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (100, 149, 237), rect, 3)
                else:
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2)

        text = font.render("Explored maze | Esc to exit", True, (50, 50, 50))
        screen.blit(text, (10, height - 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        clock.tick(60)

    pygame.quit()

def checkalreadysearched(coords):
    if coords in alreadysearched:
        return False
    alreadysearched[coords] = True
    return True

def addfrontier(matrix, coord):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new = (coord[0] + dx, coord[1] + dy)
        if 0 <= new[0] < len(matrix) and 0 <= new[1] < len(matrix[0]) and matrix[new[0]][new[1]] == 0:
            if checkalreadysearched(new):
                stack.append(new)
                parent[new] = coord

def tofrontier():
    global start
    start = stack.pop()

def checker():
    return start == end

def reconstructpath():
    current = end
    while current != checkstart:
        path[current] = True
        current = parent.get(current)
        if current is None:
            break
    path[checkstart] = True

checkalreadysearched(start)
addfrontier(maze_array, start)

while stack:
    tofrontier()
    if checker():
        print("solved ig")

        reconstructpath()
        break
    addfrontier(maze_array, start)

if start == end:
    display_explored_maze(maze_array, alreadysearched, checkstart, end)
else:
    print("UNSOLVABLE")
    display_explored_maze(maze_array, alreadysearched, checkstart, end)