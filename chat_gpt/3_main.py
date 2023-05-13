import pygame
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

# Define grid properties
n = 50
cell_size = 10
grid = [[0 for _ in range(n)] for _ in range(n)]
fire_spread_prob = 0.3
fire_duration = 30
grass_regrow_duration = 50

# Initialize Pygame
pygame.init()

# Set up the display window
width = n * cell_size
height = n * cell_size
screen = pygame.display.set_mode((width, height))

# Set up the font for displaying countdowns
font = pygame.font.SysFont("arial", 10)

# Set up the clock for controlling the framerate
clock = pygame.time.Clock()

# Draw the grid on the screen
def draw_grid():
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                pygame.draw.rect(screen, GREEN, (i * cell_size, j * cell_size, cell_size, cell_size))
            elif grid[i][j] == 1:
                pygame.draw.rect(screen, BROWN, (i * cell_size, j * cell_size, cell_size, cell_size))
            elif grid[i][j] == 2:
                pygame.draw.rect(screen, ORANGE, (i * cell_size, j * cell_size, cell_size, cell_size))
            elif grid[i][j] == 3:
                pygame.draw.rect(screen, RED, (i * cell_size, j * cell_size, cell_size, cell_size))

# Spread fire to adjacent grass cells
def spread_fire(i, j):
    if i > 0 and grid[i-1][j] == 1 and random.random() < fire_spread_prob:
        grid[i-1][j] = 2
    if i < n-1 and grid[i+1][j] == 1 and random.random() < fire_spread_prob:
        grid[i+1][j] = 2
    if j > 0 and grid[i][j-1] == 1 and random.random() < fire_spread_prob:
        grid[i][j-1] = 2
    if j < n-1 and grid[i][j+1] == 1 and random.random() < fire_spread_prob:
        grid[i][j+1] = 2

# Regrow grass on adjacent earth cells
def regrow_grass(i, j):
    if i > 0 and grid[i-1][j] == 1:
        grid[i-1][j] = 0
    if i < n-1 and grid[i+1][j] == 1:
        grid[i+1][j] = 0
    if j > 0 and grid[i][j-1] == 1:
        grid[i][j-1] = 0
    if j < n-1 and grid[i][j+1] == 1:
        grid[i][j+1] = 0

# # Main game loop
# running = True
# placing = 0
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event

# Main game loop
running = True
placing = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = pos[0] // cell_size, pos[1] // cell_size
            if placing == 0:
                grid[x][y] = 1
            elif placing == 1:
                grid[x][y] = 2
            elif placing == 2:
                grid[x][y] = 3
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start the simulation
                for i in range(n):
                    for j in range(n):
                        if grid[i][j] == 2:
                            grid[i][j] = 3
                        elif grid[i][j] == 3:
                            grid[i][j] = 1
                for i in range(n):
                    for j in range(n):
                        if grid[i][j] == 0:
                            spread_fire(i, j)
                        elif grid[i][j] == 1:
                            regrow_grass(i, j)
                for i in range(n):
                    for j in range(n):
                        if grid[i][j] == 2:
                            grid[i][j] = 1
                        elif grid[i][j] == 3:
                            grid[i][j] -= 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                placing = 0
            elif event.key == pygame.K_2:
                placing = 1
            elif event.key == pygame.K_3:
                placing = 2

    # Clear the screen
    screen.fill(WHITE)

    # Update the countdowns and switch cell states if necessary
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2:
                grid[i][j] = 3
            elif grid[i][j] == 3:
                grid[i][j] = 1
            elif grid[i][j] == 1:
                grid[i][j] -= 1
            elif grid[i][j] == -1:
                grid[i][j] = 0

    # Draw the grid
    draw_grid()

    # Draw the countdowns on the cells
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 or grid[i][j] == 2:
                text = font.render(str(grid[i][j]), True, BLACK)
                screen.blit(text, (i * cell_size + 2, j * cell_size + 2))

    # Draw the current placing color indicator
    if placing == 0:
        color = GREEN
    elif placing == 1:
        color = BROWN
    elif placing == 2:
        color = ORANGE
    pygame.draw.rect(screen, color, (0, height-20, 20, 20))

    # Update the display
    pygame.display.flip()

    # Control the framerate
    clock.tick(30)

# Quit Pygame
pygame.quit()
