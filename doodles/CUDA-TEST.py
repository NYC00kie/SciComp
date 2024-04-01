import numpy as np
from numba import cuda, vectorize
import time
from PIL import Image
from datetime import datetime
import cv2




# CUDA kernel to compute Mandelbrot set
@cuda.jit
def mandelbrot_kernel(real, imag, max_iter, output):
    start_x, start_y = cuda.grid(2)
    stride_x, stride_y = cuda.gridsize(2)
    height, width, depth = output.shape

    for x in range(start_x, width, stride_x):
        for y in range(start_y, height, stride_y):
            c_real = real[x]
            c_imag = imag[y]
            z_real = 0.0
            z_imag = 0.0
            iterations = 0
            while (z_real * z_real + z_imag * z_imag) <= 4.0 and iterations < max_iter:
                temp_real = z_real * z_real - z_imag * z_imag + c_real
                z_imag = 2.0 * z_real * z_imag + c_imag
                z_real = temp_real
                iterations += 1
            output[y, x] = (iterations % 256, iterations % 128 * 2, iterations % 64 * 4, 255)
def main():
    # Define the size of the array (image)
    width = 50000
    height = 50000
    max_iter = 10000

    # Generate complex coordinates for the image
    real = np.linspace(-2, 1, width, dtype=np.float32)
    imag = np.linspace(-1, 1, height, dtype=np.float32)

    # Allocate memory for the output image on the GPU
    d_output = cuda.device_array((width, height, 4), dtype=np.uint8)

    # Time GPU computation
    start_time = time.time()

    # Configure kernel launch parameters
    threads_per_block = (16, 16)
    blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Launch kernel
    mandelbrot_kernel[blocks_per_grid, threads_per_block](real, imag, max_iter, d_output)

    # Synchronize threads
    cuda.synchronize()

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print("Time taken for GPU computation: {:.6f} seconds".format(elapsed_time))

    # Copy the result back to the CPU
    result = d_output.copy_to_host()

    print(len(result))

    # Plot Mandelbrot set (if needed)
    file_name = "test"
    img = Image.fromarray(result, mode="RGBA") 
    rgb_im = img.convert('RGB')

    rgb_im.save(file_name+".JPEG","JPEG")
    #img.save(file_name+".PNG","PNG")



if __name__ == "__main__":
    main()