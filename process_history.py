#!/usr/bin/env python
import json
import sys

import matplotlib.pyplot as plot
import gudhi

TRIVIAL_HOLES = {
    (3, (1.4142135623730951, 1.7320508075688772)),
    (1, (1.0, 1.4142135623730951)),
    (0, (0.0, 1.0)),
}

def history_to_points(history):
    points = []
    for z, grid in enumerate(history):
        # print()
        for y, row in enumerate(grid):
            # print(row)
            for x, tile in enumerate(row):
                if tile != 2:
                    points.append((x, y, z))

    return points


def process_history(history):
    print(f"History length: {len(history)}")
    points = history_to_points(history)
    del history

    print("Creating Rips Complex")
    # rips = gudhi.RipsComplex(points=points, max_edge_length=2.1, sparse=0.25)
    rips = gudhi.RipsComplex(points=points, max_edge_length=2.1)

    print("Creating simplex tree")
    simplex_tree = rips.create_simplex_tree(max_dimension=4)

    print("Running simplex_tree.persistence()")
    # diag = simplex_tree.persistence(homology_coeff_field=2, min_persistence=0)
    diag = simplex_tree.persistence()
    # print("diag=", diag)

    diag = [d for d in diag if d not in TRIVIAL_HOLES]

    gudhi.plot_persistence_diagram(diag)
    # gudhi.plot_persistence_barcode(diag, max_intervals=0)
    plot.show()


def main():
    if len(sys.argv) != 2:
        print("Missing history...")
        return

    with open(sys.argv[1], "r") as file:
        history = json.load(file)

    process_history(history)


if __name__ == "__main__":
    main()
