from functools import partial
from multiprocessing import Array, Pool, cpu_count

import matplotlib.pyplot as plt
import numpy as np
import yeast_cells
from KONSTANTS import *
from scipy.signal import convolve2d
from yeast_cells import do_cell

def diffuse(grid_part):
    p = 0.125
    kernel = np.ones((3, 3)) * p
    kernel[1, 1] = 0

    grid_part = convolve2d(grid_part, kernel, mode="same", boundary="wrap")

    return grid_part


def main_cpu():
    np.random.seed(0)
    # creating diffusion kernel
    p = 0.125
    kernel = np.ones((3, 3)) * p
    kernel[1, 1] = 0


    dim = (materials, width, height)

    grid = np.zeros(dim, dtype=np.float64)

    cells = [[0.0 for n in range(cell_parameters)] for _ in range(cells_n)]


    cells[0][0] = 0
    cells[0][1] = 0
    cells[0][2] = 0
    cells[0][3] = 1
    cells[0][4] = 0
    cells[0][5] = 1
    cells[0][6] = 1.1
    cells[0][7] = 1
    cells[0][8] = 2
    cells[0][9] = 2
    cells[0][10] = 0
    cells[0][11] = 0.5
    cells[0][12] = 1/30
    cells[0][13] = 1/7200
    cells[0][14] = 0.01
    cells[0][15] = 0.2
    cells[0][16] = 1/3900
    cells[0][17] = 0
    cells[0][18] = cells[0][3]

    print(len(cells[0]))

    grid[0] = np.full((width, height), 36) * 10e-3
    grid[1] = np.full((width, height), 100) * 10e-3

    # construct a multiprocess-safe array
    flattened_grid = grid.ravel()
    thread_grid = Array("d", flattened_grid.size, lock=True)
    np.frombuffer(thread_grid.get_obj(), dtype="float")[:] = flattened_grid

    yeast_cells.grid = np.frombuffer(thread_grid.get_obj(),  dtype="float").reshape(dim)

    dead = 0
    alive = 1

    """  von hier an ist die Reihenfolge der Schritte aus dem 'Paper
    INDISIM-YEAST: an individual-based simulator on a website for 
    experimenting and investigating diverse dynamics of yeast 
    populations in liquid media' zu beachten:

    s-random motion
    s-uptake of nutrient particles
    s-enough nutrient particles for maintanance?
    s-Enough nutrient particles for new biomass?
    s-production and excretion of ethanole
    s-buding phase?
    -cell division, new yeast cell (mutation!)
    -unbudded phase
    -requirments to be viable?
    -update of new individual characteristics (wdym?)
    -repeat
    """
    tracking_params = {
    0:[],
    1:[],
    2:[],
    3:[]
    }
    try:
        print(iterations)
        with Pool(32) as p:
            for i in range(iterations):
                if i % loggingit == 0:
                    print(f"Glucose:{np.sum(yeast_cells.grid[0])}")
                    print(f"Oxy:{np.sum(yeast_cells.grid[1])}")
                    print(f"Ethanol:{np.sum(yeast_cells.grid[2])}")
                    print(f"CO_2:{np.sum(yeast_cells.grid[3])}")
                    print(f"iterations:{i}")

                # diffuse material
                for j in range(diff_per_it):
                    yeast_cells.grid[:] = p.map(diffuse, yeast_cells.grid)


                if i % loggingit == 0:
                    for entry in range(materials):
                        plt.imshow(yeast_cells.grid[entry])
                        plt.colorbar()
                        plt.savefig(f"./out/grid_post_{entry}_{i//loggingit}.jpg", dpi=800)
                        plt.clf()

                # do the cell, yes I said it.
                do_cell_with_grid = partial(do_cell, dim=dim)
                all_cells = p.map(do_cell_with_grid, cells)

                # print(possibly_new_cells, cells)
                cells = []
                for part_of_cells in all_cells:
                    cells.extend(part_of_cells)

                cells_new = [cell for cell in cells if np.sum(cell) != 0]

                alive = len(cells_new)
                dead += len(cells) - len(cells_new)

                cells = cells_new

                tracking_params[0].append(alive)
                tracking_params[1].append(dead)
                tracking_params[2].append(np.sum(yeast_cells.grid[0]))
                tracking_params[3].append(np.sum(yeast_cells.grid[1]))


    except Exception as e:
        print(e)
    finally:
        for i in range(len(tracking_params)):
            plt.plot(np.arange(len(tracking_params[i])),tracking_params[i])
            plt.savefig(f"cell_params_{i}.jpg")
            plt.clf()


if __name__ == "__main__":
    main_cpu()
