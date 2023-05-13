import pygame


# Set the dimensions of each cell and the grid size
CELL_WIDTH = 10
CELL_HEIGHT = 10
GRID_SIZE = 50
WINDOW_SIZE = (CELL_WIDTH * GRID_SIZE, CELL_HEIGHT * GRID_SIZE)

FRAMERATE = 30

WATER = 0
EARTH = 1
FIRE = 2
GRASS = 3
COLORS = {
    WATER: (0, 0, 255),
    EARTH: (0, 0, 0),
    FIRE: (255, 0, 0),
    GRASS: (0, 255, 0),
}


# Define the function for drawing the grid
def draw_grid(screen, grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_color = COLORS[grid[x][y]]
            pygame.draw.rect(screen, cell_color, (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


def update_grid(grid):
    new_earth_cells = set()
    new_fire_cells = set()
    new_grass_cells = set()

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell = grid[x][y]
            if cell == EARTH:
                new_grass_cells.add((x, y))
            if cell == FIRE:
                new_earth_cells.add((x, y))
            if cell == GRASS:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if x + dx < 0 or x + dx >= GRID_SIZE or y + dy < 0 or y + dy >= GRID_SIZE:
                            continue
                        if grid[x + dx][y + dy] == FIRE:
                            new_fire_cells.add((x, y))

    for x, y in new_earth_cells:
        grid[x][y] = EARTH
    for x, y in new_fire_cells:
        grid[x][y] = FIRE
    for x, y in new_grass_cells:
        grid[x][y] = GRASS


def main():
    print("Initializing simulation.")
    pygame.init()
    pygame.display.set_caption("Fire Simulation")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    # Init the grid to all grass
    # TODO Load the grid from a file
    grid = [[GRASS for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    mouse_down = False
    active_coloring_tile = GRASS
    simulation_active = False

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
                if event.key == pygame.K_1:
                    active_coloring_tile = EARTH
                elif event.key == pygame.K_2:
                    active_coloring_tile = FIRE
                elif event.key == pygame.K_3:
                    active_coloring_tile = GRASS
                elif event.key == pygame.K_4:
                    active_coloring_tile = WATER
                elif event.key == pygame.K_SPACE:
                    simulation_active = not simulation_active

        # Handle mouse input
        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            cell_x = mouse_pos[0] // CELL_WIDTH
            cell_y = mouse_pos[1] // CELL_HEIGHT
            grid[cell_x][cell_y] = active_coloring_tile

        if simulation_active:
            update_grid(grid)

        draw_grid(screen, grid)
        # Update the screen and wait for the next frame
        pygame.display.flip()
        clock.tick(FRAMERATE)

    # Quit Pygame
    pygame.quit()
    print("Simulation finished.")


if __name__ == "__main__":
    main()
