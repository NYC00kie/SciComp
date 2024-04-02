import numpy as np
from numba import cuda, vectorize
import time
from PIL import Image
from datetime import datetime
import cv2
import matplotlib.pyplot as plt




# CUDA kernel to compute Mandelbrot set
@cuda.jit
def diffusion_kernal(real, imag, max_iter, output):
    start_x, start_y = cuda.grid(2)
    stride_x, stride_y = cuda.gridsize(2)
    height, width, depth = output.shape

    for x in range(start_x, width, stride_x):
        for y in range(start_y, height, stride_y):
            pass

def main():
    # Define the size of the array (image)
    width = 100
    height = 100

    cells_n = 10000

    # Allocate memory for the output on the GPU
    #
    # width x height
    # Ethanol, Sauerstoff, Zucker, Cell ID
    #

    grid = np.random.randint(0,20,size=(width, height,3), dtype=np.uint16)

	plt.imshow(grid)
	plt.colorbar()
	plt.savefig("grid_pre.jpg")
	plt.clf()

    d_grid = cuda.to_device(grid)

    #
    # cells_n x 14 paramters
    # 
    #
    #

    yeast_cells = np.random.rand(cells_n, 15, dtype=np.float16)

    print(yeast_cells)

    d_yeast_cells = cuda.to_device(yeast_cells)

    # Time GPU computation
    start_time = time.time()

    # Configure kernel launch parameters
    threads_per_block = (16, 16)
    blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Launch kernel
    diffusion_kernel[blocks_per_grid, threads_per_block](d_grid)

    # Synchronize threads
    cuda.synchronize()

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print("Time taken for GPU computation: {:.6f} seconds".format(elapsed_time))

    # Copy the result back to the CPU
    result = d_grid.copy_to_host()

    print(len(result))

	plt.imshow(result)
	plt.colorbar()
	plt.savefig("grid_post.jpg")
	plt.clf()



if __name__ == "__main__":
    main()