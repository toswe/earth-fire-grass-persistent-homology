import pygame
import random
import json
from datetime import datetime
import sys

# Set the dimensions of each cell and the grid size
CELL_WIDTH = 10
CELL_HEIGHT = 10
GRID_SIZE = 50
WINDOW_SIZE = (CELL_WIDTH * GRID_SIZE, CELL_HEIGHT * GRID_SIZE)

FRAMERATE = 30
SIMPLE_COLORS = False
TEXT_COLOR = (255, 255, 255)

# Types
WATER = 0
EARTH = 1
FIRE = 2
GRASS = 3
TYPE_TO_COLOR = {
    WATER: (0, 0, 255),
    EARTH: (0, 0, 0),
    FIRE: (255, 0, 0),
    GRASS: (0, 255, 0),
}
TYPE_TO_TEXT = {
    WATER: "WATER",
    EARTH: "EARTH",
    FIRE: "FIRE",
    GRASS: "GRASS",
}

EARTH_LIFESPAN = 30
FIRE_LIFESPAN = 30
FIRE_PROBABILITY = 0.1

# TODO Create tile class
# Tiles
EARTH_TILE = {
    "type": EARTH,
    "lifespan": EARTH_LIFESPAN,
    "next_type": GRASS,
}
FIRE_TILE = {
    "type": FIRE,
    "lifespan": FIRE_LIFESPAN,
    "next_type": EARTH,
}
GRASS_TILE = {
    "type": GRASS,
    "lifespan": -1,
}
WATER_TILE = {
    "type": WATER,
    "lifespan": -1,
}
TYPE_TO_TILE = {
    WATER: WATER_TILE,
    EARTH: EARTH_TILE,
    FIRE: FIRE_TILE,
    GRASS: GRASS_TILE,
}


def get_color_pretty(tile):
    base_color = TYPE_TO_COLOR[tile["type"]]
    # TODO Transition colors by avereging color tuples (numpy needed)
    if tile["type"] == FIRE:
        color_offset = (FIRE_LIFESPAN - tile["lifespan"]) * 255 / FIRE_LIFESPAN
        return (
            base_color[0] - color_offset,
            base_color[1],
            base_color[2],
        )
    if tile["type"] == EARTH:
        color_offset = (EARTH_LIFESPAN - tile["lifespan"]) * 255 / EARTH_LIFESPAN
        return (
            base_color[0],
            base_color[1] + color_offset,
            base_color[2],
        )
    # TODO Add pretty colors for grass and water
    return base_color


def get_color_simple(tile):
    return TYPE_TO_COLOR[tile["type"]]


def get_color(tile):
    return get_color_simple(tile) if SIMPLE_COLORS else get_color_pretty(tile)


# Define the function for drawing the grid
def draw_grid(screen, grid):
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            cell_color = get_color(tile)
            pygame.draw.rect(
                screen,
                cell_color,
                (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT),
            )


def set_fire(tile):
    if random.random() < FIRE_PROBABILITY:
        tile["next_type"] = FIRE
        tile["lifespan"] = 0
    return tile


def update_grid(grid):
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile["type"] == GRASS:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if (
                            x + dx < 0
                            or x + dx >= GRID_SIZE
                            or y + dy < 0
                            or y + dy >= GRID_SIZE
                        ):
                            continue
                        if grid[x + dx][y + dy]["type"] == FIRE:
                            tile.update(set_fire(tile))

    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile["lifespan"] == 0:
                tile.update(TYPE_TO_TILE[tile["next_type"]])
            elif tile["lifespan"] > 0:
                tile["lifespan"] -= 1


# TODO Maybe needed for history?
# def grid_to_matrix(grid):
#     return [[tile['type'] for tile in row] for row in grid]


def get_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_grid(grid):
    file_path = f"./saves/{get_time()}.json"
    with open(file_path, "w") as file:
        json.dump(grid, file)
    return file_path


def create_default_grid():
    return [[GRASS_TILE.copy() for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]


def load_grid(file_path):
    with open(file_path) as file:
        return json.load(file)


def main():
    print("Initializing simulation.")
    pygame.init()
    pygame.display.set_caption("Fire Simulation")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    if len(sys.argv) == 2:
        grid = load_grid(sys.argv[1])
    else:
        grid = create_default_grid()

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
                elif event.key == pygame.K_c:
                    global SIMPLE_COLORS
                    SIMPLE_COLORS = not SIMPLE_COLORS
                elif event.key == pygame.K_s:
                    save_grid(grid)

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
        text = font.render(message, True, TEXT_COLOR)
        screen.blit(text, [0, 0])
        # Update the screen and wait for the next frame
        pygame.display.flip()
        clock.tick(FRAMERATE)

    # Quit Pygame
    pygame.quit()
    print("Simulation finished.")


if __name__ == "__main__":
    main()
