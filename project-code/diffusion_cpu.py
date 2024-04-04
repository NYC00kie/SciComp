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
    width = 100
    height = 100

    cells_n = 10000
    iterations = 101
    entries = 1

    p = 0.1
    kernel = np.ones((3, 3)) * p
    kernel[1, 1] = 1 - (8 * p)

    dim = (entries,width,height)
    
    grid = np.random.randint(0, 800, size=dim, dtype=np.float16)

    yeast_cells = np.random.rand(cells_n, 15)

    plt.imshow(grid_in[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

    for i in range(iterations):

        grid = convolve2d(grid_in, kernel, mode="same", boundary="wrap")

        print(np.sum(grid))

        for entri in range(entries):

            if i % 10 == 0:
                plt.imshow(grid_out[entri])
                plt.colorbar()
                plt.savefig(f"grid_post_{entri}_{i}.jpg")
                plt.clf()



if __name__ == "__main__":
 
    main_cpu()
