# Earth-fire-grass-persistent-homology

This is a modified python simlation of a the earth fire grass evolutionary game described in the paper
[Persistent homology and the shape of evolutionary games](https://www.sciencedirect.com/science/article/pii/S0022519321003222).

The simulation is almost identical to the original apart from the water tile added to this version.

Earth-Fire-Grass is a cyclical SIRS (Susceptible-Infectious-Recovered-Susceptible)
model played on a finite 2D square lattice. It has three simple rules:

1. When fire burns out, determined by `FIRE_LIFESPAN`, it turns into earth
2. When earth is fertile, determined by `EARTH_LIFESPAN`, it turns into grass
3. Fire burns grass

Fire randomly selects one tile among neighbors that are grass, and sets it on fire.
This means that if there is a single grass in the neighborhood of a fire tile,
the grass tile will be set on fire with probability = 1.
This selection mechanism is the only source of randomness in the game.

The water tile stays the same through out the simulation.

## Requirements

Python 3.10.4 was used for this project.

## Running locally

0. Create a virtual environment (optional step):
    ```
    virtualenv env
    source env/bin/activate
    ```

1. Installing the required libraries:
    ```
    pip install -r requirements.txt
    ```

2. Run the script with:
    ```
    python main.py
    ```

## Examples

TODO

## Instructions

Keyboard controls:
```
SPACE - Start/Stop the simulation

1 - Select Earth tile
2 - Select Fire tile
3 - Select Grass tile
4 - Select Water tile

C - Toggle graphics
S - Save current simulation state
```

### Configuration

Simulation configuration is saved in the `CONFIGURATION` variable, and is stored when saving.
It contains the folowing:
```
GRID_SIZE - Size of the grid used in the simulation
TILE_LIFESPAN - Lifespan of earth and fire tiles
SAVE_HISTORY - Boolean flag indicating if history should be saved
PROCESS_HISTORY - Boolean flag indicating if history should be proccessed after simulation ends
FRAMERATE - Representing the frames per second for the simulation
RECORD_GAME - Boolean flag indicating if the game should be recorded
MAX_ITERATIONS - Maximum number of iterations (set to -1 if not used)
```

### Saving

By pressing the `s` key you save the state of the project as a `.json` file located in the
`saves` directory. The name of the save will be the time at witch the script was started.

If you are running the simulation from a previously saved file and try to save,
the loaded save file will be overwritten.

### Loading saves

You can start a simulation from a save file by running the following command:

```
python main.py ./saves/name_of_the_save.json
```

### History

If the `SAVE_HISTORY` flag is set to `True` each iteration of the simulation will be saved.
The location of the file will be in the `history` directory.

### Recording

If the `RECORD_GAME` flag is set to `True` the simulation will be recorded as a `.gif` file.
The location of the file will be in the `recordings` directory.

### History processing

The topological analysis of the simulation is done in the `process_history.py` script:
```
python process_history.py history/example_simulation.json
```

Alternatevely the `PROCESS_HISTORY` flag can be set to `True` and the history will be processed
right after the simulation ends.

In the original paper they used the Vietoris Rips complex for data analysis,
but in this implementation the Alpha complex was used,
because the VR complex turned out to be too memory and CPU intensive.

Also, here instad of analyzing the topology of the fires,
the topology of the complement space was used.

#### Processing results

The result of the processing are the following graphs:

1. The persistance diagram of the data topology
2. The barcode persistance diagram of the data topology
3. The rendering of the 3D space ocupied by the fire tiles
