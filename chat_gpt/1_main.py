# Generated with chat GPT4
# Link to conversation:
# https://chat.openai.com/share/55b09cc0-3b90-4de3-91fe-b5c548017a55

import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Set the dimensions of each cell and the grid size
CELL_WIDTH = 10
CELL_HEIGHT = 10
GRID_SIZE = 50

# Initialize Pygame
pygame.init()

# Set the window size
WINDOW_SIZE = (CELL_WIDTH * GRID_SIZE, CELL_HEIGHT * GRID_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the window title
pygame.display.set_caption("Fire Simulation")

# Create the initial grid with all grass cells
grid = [[GREEN for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Set up the simulation variables
burning_cells = set()
earth_cells = set()
fire_cells = set()

# Set up the event variables
mouse_down = False
space_down = False

# Define the function for checking if a cell is on fire
def is_on_fire(x, y):
    return (x, y) in burning_cells or (x, y) in fire_cells

# Define the function for updating the grid
def update_grid():
    global burning_cells, earth_cells, fire_cells
    new_burning_cells = set()
    new_earth_cells = set()
    new_fire_cells = set()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == GREEN:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if x + dx < 0 or x + dx >= GRID_SIZE or y + dy < 0 or y + dy >= GRID_SIZE:
                            continue
                        if grid[x + dx][y + dy] == ORANGE or grid[x + dx][y + dy] == RED:
                            if random.random() < 1:
                                new_burning_cells.add((x, y))
                                break
                if (x, y) not in new_burning_cells:
                    new_earth_cells.add((x, y))
            elif grid[x][y] == ORANGE:
                new_fire_cells.add((x, y))
            elif grid[x][y] == RED:
                new_earth_cells.add((x, y))
    burning_cells = new_burning_cells
    earth_cells = new_earth_cells
    fire_cells = new_fire_cells
    for x, y in burning_cells:
        grid[x][y] = ORANGE
    for x, y in earth_cells:
        grid[x][y] = GREEN
    for x, y in fire_cells:
        grid[x][y] = RED

# Define the function for drawing the grid
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_color = grid[x][y]
            pygame.draw.rect(screen, cell_color, (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

# Main game loop
done = False
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_down = False

    # Handle mouse input
    if mouse_down:
        mouse_pos = pygame.mouse.get_pos()
        cell_x = mouse_pos[0] // CELL_WIDTH
        cell_y = mouse_pos[1] // CELL_HEIGHT
        if grid[cell_x][cell_y] == GREEN:
            grid[cell_x][cell_y] = ORANGE
        elif grid[cell_x][cell_y] == ORANGE:
            grid[cell_x][cell_y] = RED
        elif grid[cell_x][cell_y] == RED:
            grid[cell_x][cell_y] = GREEN

    # Update the grid and draw it
    if space_down:
        update_grid()
    draw_grid()

    # Update the screen and wait for the next frame
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
