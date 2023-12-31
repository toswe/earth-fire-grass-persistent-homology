import random
import json
from datetime import datetime
import sys
from pprint import pprint

import pygame
from pygame_screen_recorder import pygame_screen_recorder as pgr

from process_history import process_history

CONFIGURATION = {
    "GRID_SIZE": 12,
    "TILE_LIFESPAN": 5,
    "SAVE_HISTORY": False,
    "PROCESS_HISTORY": False,
    "FRAMERATE": 30,
    "RECORD_GAME": False,
    "MAX_ITERATIONS": -1,
}

SIMPLE_COLORS = False

WINDOW_EDGE_SIZE = 500
CELL_SIZE = 0
WINDOW_SIZE = 0

DEFAULT_FILE_PATH = f"./saves/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
TEXT_COLOR = (255, 255, 255)


# TODO Implement this better
def init_globals():
    global CELL_SIZE
    CELL_SIZE = WINDOW_EDGE_SIZE // CONFIGURATION["GRID_SIZE"]
    global WINDOW_SIZE
    WINDOW_SIZE = (
        CELL_SIZE * CONFIGURATION["GRID_SIZE"],
        CELL_SIZE * CONFIGURATION["GRID_SIZE"],
    )
    global EARTH_LIFESPAN
    global FIRE_LIFESPAN
    global EARTH_TILE
    global FIRE_TILE
    global TYPE_TO_TILE

    EARTH_LIFESPAN = CONFIGURATION["TILE_LIFESPAN"]
    FIRE_LIFESPAN = CONFIGURATION["TILE_LIFESPAN"]

    EARTH_TILE = {
        "type": EARTH,
        "lifespan": EARTH_LIFESPAN,
    }
    FIRE_TILE = {
        "type": FIRE,
        "lifespan": FIRE_LIFESPAN,
    }

    TYPE_TO_TILE = {
        WATER: WATER_TILE,
        EARTH: EARTH_TILE,
        FIRE: FIRE_TILE,
        GRASS: GRASS_TILE,
    }


# Types
WATER = 0
EARTH = 1
FIRE = 2
GRASS = 3

EARTH_LIFESPAN = CONFIGURATION["TILE_LIFESPAN"]
FIRE_LIFESPAN = CONFIGURATION["TILE_LIFESPAN"]

# Depricated
FIRE_PROBABILITY = 0.1

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

TYPE_TRANSITIONS = {
    WATER: WATER,
    EARTH: GRASS,
    FIRE: EARTH,
    GRASS: FIRE,
}

# TODO Create tile class
# Tiles
EARTH_TILE = {
    "type": EARTH,
    "lifespan": EARTH_LIFESPAN,
}
FIRE_TILE = {
    "type": FIRE,
    "lifespan": FIRE_LIFESPAN,
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
        color_offset = (FIRE_LIFESPAN - tile["lifespan"]) * 255 / (FIRE_LIFESPAN or 1)
        return (
            base_color[0] - color_offset,
            base_color[1],
            base_color[2],
        )
    if tile["type"] == EARTH:
        color_offset = (EARTH_LIFESPAN - tile["lifespan"]) * 255 / (EARTH_LIFESPAN or 1)
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
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )


def set_fire(tile):
    tile["lifespan"] = 0


# Depricated
def old_fire_handle(grid, x, y, tile):
    if tile["type"] == GRASS:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (
                    x + dx < 0
                    or x + dx >= CONFIGURATION["GRID_SIZE"]
                    or y + dy < 0
                    or y + dy >= CONFIGURATION["GRID_SIZE"]
                ):
                    continue
                if grid[x + dx][y + dy]["type"] == FIRE:
                    if random.random() < FIRE_PROBABILITY:
                        set_fire(tile)


def new_fire_handle(grid, x, y, tile):
    if tile["type"] == FIRE:
        neighbour_grass = list()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (
                    x + dx < 0
                    or x + dx >= CONFIGURATION["GRID_SIZE"]
                    or y + dy < 0
                    or y + dy >= CONFIGURATION["GRID_SIZE"]
                ):
                    continue

                if grid[x + dx][y + dy]["type"] == GRASS:
                    neighbour_grass.append(grid[x + dx][y + dy])

        if len(neighbour_grass) > 0:
            grass = random.choice(neighbour_grass)
            set_fire(grass)


def update_grid(grid):
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            # old_fire_handle(grid, x, y, tile)
            new_fire_handle(grid, x, y, tile)

    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile["lifespan"] == 0:
                tile.update(TYPE_TO_TILE[TYPE_TRANSITIONS[tile["type"]]])
            elif tile["lifespan"] > 0:
                tile["lifespan"] -= 1


def grid_to_matrix(grid):
    return [[tile["type"] for tile in row] for row in grid]


def save_simulation(grid, file_path):
    with open(file_path, "w") as file:
        save_obj = {
            "config": CONFIGURATION,
            "matrix": grid_to_matrix(grid),
        }
        json.dump(save_obj, file, indent=4)
    return file_path


def create_default_grid():
    size = CONFIGURATION["GRID_SIZE"]
    return [[GRASS_TILE.copy() for x in range(size)] for y in range(size)]


def load_simulation(file_path):
    with open(file_path) as file:
        save_obj = json.load(file)

    global CONFIGURATION
    CONFIGURATION = save_obj["config"]

    init_globals()
    return [
        [TYPE_TO_TILE[tile_type].copy() for tile_type in row]
        for row in save_obj["matrix"]
    ]


def main():
    file_path = DEFAULT_FILE_PATH
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        grid = load_simulation(file_path)
    else:
        grid = create_default_grid()

    print("Initializing simulation with following config:")
    pprint(CONFIGURATION)

    init_globals()
    pygame.init()
    pygame.display.set_caption("Fire Simulation")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    if CONFIGURATION["RECORD_GAME"]:
        recorder = pgr(f"recordings/{file_path.split('/')[-1].split('.')[0]}.gif")

    if CONFIGURATION["SAVE_HISTORY"] or CONFIGURATION["PROCESS_HISTORY"]:
        history = []

    mouse_down = False
    active_coloring_type = GRASS
    simulation_active = False

    # Main game loop
    done = False
    iteration = 0
    while not done:
        if iteration == CONFIGURATION["MAX_ITERATIONS"]:
            break

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
                    save_simulation(grid, file_path)

        # Handle mouse input
        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            cell_x = mouse_pos[0] // CELL_SIZE
            cell_y = mouse_pos[1] // CELL_SIZE
            grid[cell_x][cell_y].update(TYPE_TO_TILE[active_coloring_type])

        if simulation_active:
            iteration += 1

            if CONFIGURATION["SAVE_HISTORY"] or CONFIGURATION["PROCESS_HISTORY"]:
                history.append(grid_to_matrix(grid))
            update_grid(grid)

            if CONFIGURATION["RECORD_GAME"]:
                recorder.click(screen)

        draw_grid(screen, grid)
        message = (
            f"Simulation active: {simulation_active}, "
            f"active coloring tile: {TYPE_TO_TEXT[active_coloring_type]}"
        )
        text = font.render(message, True, TEXT_COLOR)
        screen.blit(text, [0, 0])
        # Update the screen and wait for the next frame
        pygame.display.flip()
        clock.tick(CONFIGURATION["FRAMERATE"])

    if CONFIGURATION["RECORD_GAME"]:
        print("Saving recording.")
        recorder.save()

    # Quit Pygame
    pygame.quit()
    print("Simulation finished.")

    # TODO Implement this better
    if CONFIGURATION["SAVE_HISTORY"]:
        if file_path != DEFAULT_FILE_PATH:
            file_path = f"./history/{file_path.split('/')[-1]}"

        print(f"Saving history to: {file_path}")

        with open(file_path, "w") as file:
            json.dump(history, file)

    if CONFIGURATION["PROCESS_HISTORY"]:
        process_history(history, file_path.split('/')[-1].split('.')[0])


if __name__ == "__main__":
    main()
