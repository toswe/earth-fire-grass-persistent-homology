import pygame
import random

# Set the dimensions of each cell and the grid size
CELL_WIDTH = 10
CELL_HEIGHT = 10
GRID_SIZE = 50
WINDOW_SIZE = (CELL_WIDTH * GRID_SIZE, CELL_HEIGHT * GRID_SIZE)

FRAMERATE = 30

# Types
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
TYPE_TO_TEXT = {
    WATER: 'WATER',
    EARTH: 'EARTH',
    FIRE: 'FIRE',
    GRASS: 'GRASS',
}

EARTH_LIFESPAN = 300
FIRE_LIFESPAN = 300
FIRE_PROBABILITY = 0.01

# TODO Maybe create a class?
# Tiles
EARTH_TILE = {
    'type': EARTH,
    'lifespan': EARTH_LIFESPAN,
    'next_type': GRASS,
}
FIRE_TILE = {
    'type': FIRE,
    'lifespan': FIRE_LIFESPAN,
    'next_type': EARTH,
}
GRASS_TILE = {
    'type': GRASS,
    'lifespan': -1,
}
WATER_TILE = {
    'type': WATER,
    'lifespan': -1,
}
TYPE_TO_TILE = {
    WATER: WATER_TILE,
    EARTH: EARTH_TILE,
    FIRE: FIRE_TILE,
    GRASS: GRASS_TILE,
}


# Define the function for drawing the grid
def draw_grid(screen, grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_color = COLORS[grid[x][y]['type']]
            pygame.draw.rect(screen, cell_color, (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


def set_fire(tile):
    if random.random() < FIRE_PROBABILITY:
        tile['next_type'] = FIRE
        tile['lifespan'] = 0
    return tile



def update_grid(grid):
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile['type'] == GRASS:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if x + dx < 0 or x + dx >= GRID_SIZE or y + dy < 0 or y + dy >= GRID_SIZE:
                            continue
                        if grid[x + dx][y + dy]['type'] == FIRE:
                            tile.update(set_fire(tile))

    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile['lifespan'] == 0:
                tile.update(TYPE_TO_TILE[tile['next_type']])
            elif tile['lifespan'] > 0:
                tile['lifespan'] -= 1


def main():
    print("Initializing simulation.")
    pygame.init()
    pygame.display.set_caption("Fire Simulation")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    # Init the grid to all grass
    # TODO Load the grid from a file
    grid = [[GRASS_TILE.copy() for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    mouse_down = False
    active_coloring_type = GRASS
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
                    active_coloring_type = EARTH
                elif event.key == pygame.K_2:
                    active_coloring_type = FIRE
                elif event.key == pygame.K_3:
                    active_coloring_type = GRASS
                elif event.key == pygame.K_4:
                    active_coloring_type = WATER
                elif event.key == pygame.K_SPACE:
                    simulation_active = not simulation_active

        # Handle mouse input
        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            cell_x = mouse_pos[0] // CELL_WIDTH
            cell_y = mouse_pos[1] // CELL_HEIGHT
            grid[cell_x][cell_y].update(TYPE_TO_TILE[active_coloring_type])

        if simulation_active:
            update_grid(grid)

        draw_grid(screen, grid)
        message = (
            f"Simulation active: {simulation_active}, "
            f"active coloring tile: {TYPE_TO_TEXT[active_coloring_type]}"
        )
        text = font.render(message, True, COLORS[EARTH])
        screen.blit(text, [0, 0])
        # Update the screen and wait for the next frame
        pygame.display.flip()
        clock.tick(FRAMERATE)

    # Quit Pygame
    pygame.quit()
    print("Simulation finished.")


if __name__ == "__main__":
    main()
