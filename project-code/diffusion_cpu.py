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

def main_cpu():

    # creating diffusion kernel
    p = 0.125
    kernel = np.ones((3, 3)) * p
    kernel[1, 1] = 0

    dim = (materials,width,height)
    
    grid = numpy.zeros(dim, dtype=np.float32)

    yeast_cells = np.random.rand(cells_n, 16)
    
    #yeast_base = [0,0,0,1e-10,0,0,1e-11,12-11,2,2,0,0.00000000001,0.5]
    # Glucose
    # Sauerstoff
    # Ethanol
    # CO_2

    grid[0] = np.random.uniform(0, 800, size=(width,height))
    grid[1] = np.random.uniform(600, 800, size=(width,height))

    yeast_cells = np.random.rand(16, cells_n)
    
    plt.imshow(grid[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

   """ von hier an ist die Reihenfolge der Schritte aus dem 'Paper
   INDISIM-YEAST: an individual-based simulator on a website for 
   experimenting and investigating diverse dynamics of yeast 
   populations in liquid media' zu beachten:
   
   s-random motion
   s-uptake of nutrient particles
   s-enough nutrient particles for maintanance?
   s-Enough nutrient particles for new biomass?
   s-production and excretion of ethanole
   -buding phase?
   -cell division, new yeast cell (mutation!)
   -unbudded phase
   -requirments to be viable?
   -update of new individual characteristics (wdym?)
   -repeat
   """

    for i in range(iterations):
        if i % 100 == 0:
            print(np.sum(grid))
        
        for entry in range(materials):

            grid[entry] = convolve2d(grid[entry], kernel, mode="same", boundary="wrap")

            if i % 10 == 0:
                    plt.imshow(grid[entry])
                    plt.colorbar()
                    plt.savefig(f"grid_post_{entry}_{i//10}.jpg")
                    plt.clf()



if __name__ == "__main__":
 
    main_cpu()
