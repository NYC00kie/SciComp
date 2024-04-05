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
    
    grid = np.random.uniform(0, 800, size=dim)

    yeast_cells = np.random.rand(cells_n, 16)

    plt.imshow(grid[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

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
