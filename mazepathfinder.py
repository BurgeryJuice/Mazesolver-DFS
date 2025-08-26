from mazebuilder import *
import pygame

path = {}
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

                if coord == start:
                    pygame.draw.rect(screen, (200, 0, 0), rect)
                elif coord == end:
                    pygame.draw.rect(screen, (200, 0, 0), rect)
                elif matrix[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                elif coord in path:
                    pygame.draw.rect(screen, (255, 255, 0), rect)  # yellow for path
                elif coord in explored:
                    pygame.draw.rect(screen, (173, 216, 230), rect)  # blue for explored
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
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        clock.tick(60)

    pygame.quit()

alreadysearched = {}

def checkalreadysearched(coords):
    global alreadysearched
    if coords in alreadysearched:
        return False
    else:
        alreadysearched[coords] = True
        return True

def check_left(matrix, coord):
    return coord[0] > 0 and matrix[coord[0]-1][coord[1]] == 0

def check_right(matrix, coord):
    return coord[0] < len(matrix)-1 and matrix[coord[0]+1][coord[1]] == 0

def check_up(matrix, coord):
    return coord[1] > 0 and matrix[coord[0]][coord[1]-1] == 0

def check_down(matrix, coord):
    return coord[1] < len(matrix[0])-1 and matrix[coord[0]][coord[1]+1] == 0

stack = []

def addfrontier(matrix, coord):
    global stack

    left = (coord[0]-1, coord[1])
    right = (coord[0]+1, coord[1])
    up = (coord[0], coord[1]-1)
    down = (coord[0], coord[1]+1)

    if check_left(matrix, coord) and checkalreadysearched(left):
        stack.append(left)
    if check_right(matrix, coord) and checkalreadysearched(right):
        stack.append(right)
    if check_up(matrix, coord) and checkalreadysearched(up):
        stack.append(up)
    if check_down(matrix, coord) and checkalreadysearched(down):
        stack.append(down)

def tofrontier(matrix, coord):
    global stack
    global start
    l = stack.pop()
    start = l

def checker(matrix, coord):
    global start
    global end
    return start == end

def sharprise(coord1, coord2):
    return coord1[0] != coord2[0] and coord1[1] != coord2[1]

def reversestorer():
    global path
    global alreadysearched
    global checkstart
    l = list(alreadysearched.keys())[::-1]
    path[end] = True
    i = 1
    beg = l[0]
    next = l[1]
    while next != checkstart:
        if not sharprise(beg, next):
            beg = next
            i+=1
            path[beg] = True
            next = l[i]
        else:
            i+=1
            next = l[i]






checkalreadysearched(start)
addfrontier(maze_array, start)

while stack:
    tofrontier(maze_array, start)
    if checker(maze_array, start):
        print("SOLVED!!")
        print("number of nodes searched:", len(alreadysearched))
        reversestorer()
        print(list(path.keys()))
        path[checkstart] = True
        display_explored_maze(maze_array, alreadysearched, start, end)
        exit(0)

    addfrontier(maze_array, start)

print("UNSOLVABLE")
display_explored_maze(maze_array, alreadysearched, start, end)
