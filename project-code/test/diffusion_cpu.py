from KONSTANTS import *
import subprocess
from numba import cuda, vectorize, jit
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
import matplotlib.pyplot as plt
import math
from multiprocessing import Pool
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

    dim = (materials,width,height)
    
    grid = np.zeros(dim,dtype=np.float64)

    yeast_cells = np.zeros((cells_n,cell_parameters),dtype=np.float64)

    yeast_cells[0][0] = 0
    yeast_cells[0][1] = 0
    yeast_cells[0][2] = 0
    yeast_cells[0][3] = 1
    yeast_cells[0][4] = 0
    yeast_cells[0][5] = 1
    yeast_cells[0][6] = 1.1
    yeast_cells[0][7] = 1
    yeast_cells[0][8] = 2
    yeast_cells[0][9] = 2
    yeast_cells[0][10] = 0
    yeast_cells[0][11] = 0.25
    yeast_cells[0][12] = 1/30
    yeast_cells[0][13] = 1/7200
    yeast_cells[0][14] = 0.01
    yeast_cells[0][15] = 0.5
    yeast_cells[0][16] = 1/3900
    yeast_cells[0][17] = 0
    yeast_cells[0][18] = yeast_cells[0][3]



    print(len(yeast_cells[0]))
    # Glucose
    # Sauerstoff
    # Ethanol
    # CO_2

    grid[0] = np.full((width,height),1800)
    grid[1] = np.full((width,height),3)

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
    1:[]
    }
    with Pool(6) as p:
        print(iterations)
        for i in range(iterations):
            if i % loggingit == 0:
                print(f"Glucose:{np.sum(grid[0])}")
                print(f"Oxy:{np.sum(grid[1])}")
                print(f"Ethanol:{np.sum(grid[2])}")
                print(f"CO_2:{np.sum(grid[3])}")
                print(yeast_cells)
                print(f"Cells:{len(yeast_cells)}")
                print(f"iterations:{i}")

            
            for j in range(diff_per_it):
                grid = p.map(diffuse,grid)

            for entry in range(materials):

                if i % loggingit == 0:
                    plt.imshow(grid[entry])
                    plt.colorbar()
                    plt.savefig(f"../out/grid_post_{entry}_{i//loggingit}.jpg",dpi=800)
                    plt.clf()

            # do the cell, yes I said it.
            alive = 0
            dead = 0
            for j in range(len(yeast_cells)):
                if np.sum(yeast_cells[j]) == 0:
                    dead += 1
                else:
                    alive += 1
                    yeast_cells = do_cell(grid,yeast_cells,j)

            tracking_params[0].append(alive)
            tracking_params[1].append(dead)

    for i in range(len(tracking_params)):
        plt.plot(np.arange(iterations),tracking_params[i])
        plt.savefig(f"cell_params_{i}.jpg")
        plt.clf()

if __name__ == "__main__":
 
    main_cpu()
