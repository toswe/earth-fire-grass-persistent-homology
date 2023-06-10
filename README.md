# Earth-fire-grass-persistent-homology

TODO add a description...

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
    pip install requirements.txt -r
    ```

2. Run the script with:
    ```
    python main.py
    ```
## Instructions

Keyboard controls:
```
space - Start/Stop the simulation

1 - Select Earth tile
2 - Select Fire tile
3 - Select Grass tile
4 - Select Water tile

c - Toggle graphics
s - Save current simulation state
```

### Saving

By pressing the `s` key you save the state of the project as a `.json` file located in the
`saves` directory. The name of the save will be the time at witch the script was started.

If you are running the simulation from a previously saved file and try to save,
the loaded save file will be overwritten.

### Loading saves

You can load a save file by running the following command:

```
python main.py ./saves/name_of_the_save.json
```

### History

If the `SAVE_HISTORY` flag is set to `True` each iteration of the simulation will be saved.
The location of the file will be in the `history` directory.
