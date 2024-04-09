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

    #yeast_cells = np.zeros((cells_n, cell_parameters))
    
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

    print(len(yeast_cells))
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
    yeast_timeline = []

    for i in range(iterations):
        if i % 1 == 0:
            print(f"Glucose:{np.sum(grid[0])}")
            print(f"Oxy:{np.sum(grid[1])}")
            print(f"Ethanol:{np.sum(grid[2])}")
            print(f"CO_2:{np.sum(grid[3])}")
            print(f"Cells:{len(yeast_cells)}")

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
            yeast_cells,grid = do_cell(grid,yeast_cells,i)
            yeast_timeline.append(yeast_cells)



if __name__ == "__main__":
 
    main_cpu()
