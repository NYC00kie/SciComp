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
    width = 1000
    height = 1000

    cells_n = 10000
    iterations = 1001
    entries = 1

    # creating diffusion kernel
    p = 0.125
    kernel = np.ones((3, 3)) * p
    kernel[1, 1] = 0

    dim = (entries,width,height)
    
    grid = np.random.uniform(0, 800, size=dim)

    yeast_cells = np.random.rand(cells_n, 15)

    plt.imshow(grid[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

    for i in range(iterations):
        if i % 100 == 0:
            print(np.sum(grid))
        
        for entri in range(entries):

            grid[entri] = convolve2d(grid[entri], kernel, mode="same", boundary="wrap")

            

            if i % 100 == 0:
                    plt.imshow(grid[entri])
                    plt.colorbar()
                    plt.savefig(f"grid_post_{entri}_{i//100}.jpg")
                    plt.clf()



if __name__ == "__main__":
 
    main_cpu()
