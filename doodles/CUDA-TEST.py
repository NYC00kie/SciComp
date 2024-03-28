import numpy as np
from numba import cuda, vectorize
import time

# CUDA kernel to add two arrays
@vectorize(['float32(float32, float32)'], target='cuda')
def add_ufunc(x, y):
    return x + y

def main():
    # Define the size of the array
    array_size = 10**10

    # Generate random input arrays
    x = np.random.rand(array_size).astype(np.float32)
    y = np.random.rand(array_size).astype(np.float32)

    # Time GPU computation
    start_time = time.time()

    # Perform addition using ufunc on GPU
    result = add_ufunc(x, y)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print("Time taken for GPU computation: {:.6f} seconds".format(elapsed_time))

    # Check the correctness of the result
    expected_result = x + y
    if np.allclose(result, expected_result):
        print("GPU computation successful!")
    else:
        print("Error: GPU computation failed!")

if __name__ == "__main__":
    main()

