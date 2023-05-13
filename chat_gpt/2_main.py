import pygame
import random

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
YELLOW = (255, 255, 0)

# Define some constants
CELL_SIZE = 20
MARGIN = 2
DELAY = 200
GRASS_GROWTH_DELAY = 5
FIRE_EXTINCTION_DELAY = 3

# Set the size of the grid
n = 30
size = (n * CELL_SIZE + (n + 1) * MARGIN, n * CELL_SIZE + (n + 1) * MARGIN)

# Create the grid
grid = [[0 for x in range(n)] for y in range(n)]

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode(size)

# Set the title of the screen
pygame.display.set_caption("Fire Simulation")

# Set the font for the timer
font = pygame.font.Font(None, 20)

# Set the timer for grass growth and fire extinction
grass_growth_timer = [[0 for x in range(n)] for y in range(n)]
fire_extinction_timer = [[0 for x in range(n)] for y in range(n)]

# Set the initial colors of the cells
for row in range(n):
    for column in range(n):
        color = WHITE
        grid[row][column] = color

# Set the cell color when clicked
def set_cell_color(pos, color):
    column = pos[0] // (CELL_SIZE + MARGIN)
    row = pos[1] // (CELL_SIZE + MARGIN)
    grid[row][column] = color

# Check if a cell is on the edge of the grid
def is_on_edge(row, column):
    return row == 0 or row == n - 1 or column == 0 or column == n - 1

# Check if a cell is grass and has a fire neighbor
def has_fire_neighbor(row, column):
    if grid[row][column] == GREEN:
        if row > 0 and grid[row - 1][column] == RED:
            return True
        if row < n - 1 and grid[row + 1][column] == RED:
            return True
        if column > 0 and grid[row][column - 1] == RED:
            return True
        if column < n - 1 and grid[row][column + 1] == RED:
            return True
    return False

# Update the grid based on the simulation rules
# def update_grid():
#     for row in range(n):
#         for column in range(n):
#             # Update the grass growth timer
#             if grid[row][column] == GREEN:
#                 if grass_growth_timer[row][column] > 0:
#                     grass_growth_timer[row][column] -= 1
#                 else:
#                     grid[row][column] = YELLOW
#                     grass_growth_timer[row][column] = GRASS_GROWTH_DELAY
#             # Update the fire extinction timer
#             if grid[row][column] == RED:
#                 if fire_extinction_timer[row][column] > 0:
#                     fire_extinction_timer[row][column] -= 1
#                 else:
#                     grid[row][column] = BROWN
#                     fire_extinction_timer[row][column] = FIRE_EXTINCTION_DELAY
#             # Check if a

# Update the grid based on the simulation rules
def update_grid():
    for row in range(n):
        for column in range(n):
            # Update the grass growth timer
            if grid[row][column] == GREEN:
                if grass_growth_timer[row][column] > 0:
                    grass_growth_timer[row][column] -= 1
                else:
                    grid[row][column] = YELLOW
                    grass_growth_timer[row][column] = GRASS_GROWTH_DELAY
            # Update the fire extinction timer
            if grid[row][column] == RED:
                if fire_extinction_timer[row][column] > 0:
                    fire_extinction_timer[row][column] -= 1
                else:
                    grid[row][column] = BROWN
                    fire_extinction_timer[row][column] = FIRE_EXTINCTION_DELAY
            # Check if a grass cell has a fire neighbor
            if has_fire_neighbor(row, column):
                if grid[row][column] == GREEN:
                    if random.random() < 0.5:
                        grid[row][column] = RED
                        fire_extinction_timer[row][column] = FIRE_EXTINCTION_DELAY
                elif grid[row][column] == YELLOW:
                    grid[row][column] = RED
                    fire_extinction_timer[row][column] = FIRE_EXTINCTION_DELAY
            # Check if an earth cell has no grass neighbor
            elif grid[row][column] == BROWN:
                if not has_grass_neighbor(row, column):
                    grid[row][column] = WHITE

# Check if an earth cell has a grass neighbor
def has_grass_neighbor(row, column):
    if grid[row][column] == BROWN:
        if row > 0 and grid[row - 1][column] == GREEN:
            return True
        if row < n - 1 and grid[row + 1][column] == GREEN:
            return True
        if column > 0 and grid[row][column - 1] == GREEN:
            return True
        if column < n - 1 and grid[row][column + 1] == GREEN:
            return True
    return False

# Set the initial state of the grid
def reset_grid():
    for row in range(n):
        for column in range(n):
            color = WHITE
            grid[row][column] = color

# Draw the grid on the screen
def draw_grid():
    for row in range(n):
        for column in range(n):
            color = grid[row][column]
            pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * column + MARGIN,
                                             (MARGIN + CELL_SIZE) * row + MARGIN,
                                             CELL_SIZE, CELL_SIZE])

# Draw the timer on the screen
def draw_timer():
    text = font.render("Press SPACE to start the simulation", True, BLACK)
    screen.blit(text, [MARGIN, size[1] - MARGIN - 20])

# # Main game loop
# done = False
# clock = pygame.time.Clock()

# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:
#                 pos = pygame.mouse.get_pos()
#                 set_cell_color(pos, GREEN)
#             elif event.button == 3:
#                 pos = pygame.mouse.get_pos()
#                 set_cell_color(pos, BROWN)
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 reset_grid()
    
#     draw_grid()
#     draw_timer

# Main game loop
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                set_cell_color(pos, RED)
            elif event.button == 3:
                pos = pygame.mouse.get_pos()
                set_cell_color(pos, BROWN)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_grid()

    # Update the grid every frame
    update_grid()

    # Draw the grid and the timer on the screen
    draw_grid()
    draw_timer()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
