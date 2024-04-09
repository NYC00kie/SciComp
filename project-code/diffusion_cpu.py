from KONSTANTS import *
from numba import cuda, vectorize, jit
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
import matplotlib.pyplot as plt
import math
# from multiprocessing import Process, Queue
from multiprocessing import shared_memory, Process, Lock
from multiprocessing import cpu_count, current_process
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

    yeast_cells = np.zeros((cells_n, cell_parameters))
   
#deine Ordnung ist besser, aber hier sind nochmal an den Realfall angepasste Werte   
"""
    yeast_base = [[
                    0,                      
                    0,                      
                    0,                        
                    1e-10,                    #    
                    0,                        #
                    1,                        #                        
                    11e-11,                   # Die Zelle muss fähig sein zu wachsen     
                    1e-10,                    # Die Zelle muss ihre Startmasse verdoppeln   
                    2,                        #
                    2,                        #
                    0,                        #
                    0.00000000001,            #            
                    0.5,                      #  
                    0.5,                      #  
                    5e-13,                    #    
                    0.1,                      #  
                    1/1600,                   #    
                    0                         #
                    ]]
    
    yeast_cells = np.array(yeast_base)
"""
    # original yeast_base = [[0, 0, 0, 1e-10, 0, 0, 1e-11, 2e-11, 2, 2, 0, 0.00000000001, 0.5, 0.5, 5e-13, 0.1, 1/1600,0]]
    yeast_cells[0][0] = 0
    yeast_cells[0][1] = 0
    yeast_cells[0][2] = 0
    yeast_cells[0][3] = 100
    yeast_cells[0][4] = 0
    yeast_cells[0][5] = 1
    yeast_cells[0][6] = yeast_cells[0][3]
    yeast_cells[0][7] = 100
    yeast_cells[0][8] = 1
    yeast_cells[0][9] = 2
    yeast_cells[0][10] = 0
    yeast_cells[0][11] = 10
    yeast_cells[0][12] = 3
    yeast_cells[0][13] = 0.5
    yeast_cells[0][14] = 1
    yeast_cells[0][15] = 0.9
    yeast_cells[0][16] = 1/1600
    yeast_cells[0][17] = 0



    print(len(yeast_cells[0]))
    # Glucose
    # Sauerstoff
    # Ethanol
    # CO_2

    grid[0] = np.random.uniform(400, 800, size=(width,height))
    grid[1] = np.random.uniform(600, 800, size=(width,height))
  
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
    17:[]
    }
    print(iterations)
    for i in range(iterations):
        if i % 1 == 0:
            print(f"Glucose:{np.sum(grid[0])}")
            print(f"Oxy:{np.sum(grid[1])}")
            print(f"Ethanol:{np.sum(grid[2])}")
            print(f"CO_2:{np.sum(grid[3])}")
            print(f"Cells:{len(yeast_cells)}")
            print(f"iterations:{i}")

        # diffuse material
        for entry in range(materials):

            if i % 1 == 0:
                plt.imshow(grid[entry])
                plt.colorbar()
                plt.savefig(f"grid_post_{entry}_{i}.jpg")
                plt.clf()


            grid[entry] = convolve2d(grid[entry], kernel, mode="same", boundary="wrap")        

        # do the cell, yes I said it.
        for i in range(len(yeast_cells)):
            yeast_cells = do_cell(grid,yeast_cells,i)
            if i == 0:
                for j in range(len(yeast_cells[0])):
                    yeast0_params[j].append(yeast_cells[0][j])

    for i in range(cell_parameters):
        plt.plot(np.arange(iterations),yeast0_params[i])
        plt.savefig(f"cell_params_{i}.jpg")
        plt.clf()

if __name__ == "__main__":
 
    main_cpu()
