from KONSTANTS import *
import subprocess
from numba import jit
import numpy as np
import matplotlib.pyplot as plt
import math
from multiprocessing import Pool
from scipy.signal import convolve2d
from yeast_cells import do_cell

def main_cpu():

    np.random.seed(0)
    # creating diffusion kernel
    p = 0.125
    kernel = np.ones((3, 3)) * p
    kernel[1, 1] = 0

    dim = (materials,width,height)
    
    grid = np.zeros(dim,dtype=np.float64)

    yeast_cells = [[0 for n in range(cell_parameters)] for _ in range(cells_n)]

    yeast_cells[0][0] = 0
    yeast_cells[0][1] = 0
    yeast_cells[0][2] = 0
    yeast_cells[0][3] = 1e-5
    yeast_cells[0][4] = 0
    yeast_cells[0][5] = 1
    yeast_cells[0][6] = 11e-6
    yeast_cells[0][7] = 1e-5
    yeast_cells[0][8] = 2
    yeast_cells[0][9] = 2
    yeast_cells[0][10] = 0
    yeast_cells[0][11] = 0.1
    yeast_cells[0][12] = 0.5
    yeast_cells[0][13] = 0.5
    yeast_cells[0][14] = 5e-13
    yeast_cells[0][15] = 0.1
    yeast_cells[0][16] = 1/1600
    yeast_cells[0][17] = 0
    yeast_cells[0][18] = yeast_cells[0][3]



    print(len(yeast_cells[0]))
    # Glucose
    # Sauerstoff
    # Ethanol
    # CO_2

    grid[0] = np.random.uniform(7, 8, size=(width,height))
    grid[1] = np.random.uniform(7, 8, size=(width,height))

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
    yeast0_params = {
    0:[],
    1:[],
    2:[],
    3:[],
    4:[],
    5:[],
    6:[],
    7:[],
    8:[],
    9:[],
    10:[],
    11:[],
    12:[],
    13:[],
    14:[],
    15:[],
    16:[],
    17:[],
    18:[]
    }
    print(iterations)
    with Pool(6) as p:
        for i in range(iterations):
            if i % loggingit == 0:
                print(f"Glucose:{np.sum(grid[0])}")
                print(f"Oxy:{np.sum(grid[1])}")
                print(f"Ethanol:{np.sum(grid[2])}")
                print(f"CO_2:{np.sum(grid[3])}")
                print(yeast_cells)
                print(f"Cells:{len(yeast_cells)}")
                print(f"Cell_len:{len(yeast_cells[0])}")
                print(f"iterations:{i}")

            # diffuse material
            for entry in range(materials):

                if i % loggingit == 0:
                    plt.imshow(grid[entry])
                    plt.colorbar()
                    plt.savefig(f"./out/grid_post_{entry}_{i//loggingit}.jpg",dpi=800)
                    plt.clf()


                grid[entry] = convolve2d(grid[entry], kernel, mode="same", boundary="wrap")        


            args = [(grid,yeast_cells,j) for j in range(len(yeast_cells))]
            # do the cell, yes I said it.
            res_ = p.starmap(do_cell,args)

            new_yeast = []

            grid = np.add(grid,res_[0][1])/2

            for j in range(len(res_[0][0])):
                new_yeast.append(res_[0][0][j])

            yeast_cells = new_yeast



    # plt.plot(yeast0_params[0],yeast0_params[1],"r.")
    # plt.savefig(f"cell_params_XY.jpg")
    # plt.clf()
    # for i in range(2,cell_parameters):
    #     plt.plot(np.arange(iterations),yeast0_params[i])
    #     plt.savefig(f"cell_params_{i}.jpg")
    #     plt.clf()

if __name__ == "__main__":
 
    main_cpu()
