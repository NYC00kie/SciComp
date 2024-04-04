from numba import cuda, vectorize, jit
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
import matplotlib.pyplot as plt
import math

@cuda.jit
def diffusion_kernel(rng_states, grid_in, grid_out, yeast_cells):
    height, width, entries = grid_in.shape
    start_x, start_y = cuda.grid(2)
    stride_x, stride_y = cuda.gridsize(2)

    sharedMemT = cuda.shared.array((100*100), dtype=np.int32)

    for entri in range(entries):
        for x in range(start_x, width, stride_x):
            for y in range(start_y, height, stride_y):
                for item_num in range(grid_in[x,y, entri]):
                    neighbor_indices = (
                        ((x - 1) % width, (y - 1) % height),
                        ((x - 1) % width, y),
                        ((x - 1) % width, (y + 1) % height),
                        (x, (y - 1) % height),
                        (x, (y + 1) % height),
                        ((x + 1) % width, (y - 1) % height),
                        ((x + 1) % width, y),
                        ((x + 1) % width, (y + 1) % height)
                    )


                    selected_neighbor = neighbor_indices[rng_states[x,y,entri, item_num]]
                    # grid_out[selected_neighbor[1], selected_neighbor[0], entri] += 1
                    cuda.syncthreads()
                    cuda.atomic.add(sharedMemT, (selected_neighbor[1] * height + selected_neighbor[0] * width + entri), 1)

    cuda.syncthreads()
    if cuda.threadIdx.x == cuda.threadIdx.y and cuda.threadIdx.x == 0:
        for entri in range(entries):
            for x in range(width):
                for y in range(height):
                    cuda.atomic.add(grid_out, (y, x, entri), sharedMemT[y * height + x * width + entri])


def main():
    width = 100
    height = 100
    cells_n = 10000
    iterations = 11

    entries = 1
    grid_in = np.random.randint(0, 800, size=(width, height, entries), dtype=np.int32)
    grid_in[0, 0] = 10000
    grid_out = np.zeros((width, height, entries), dtype=np.int32)
    yeast_cells = np.random.rand(cells_n, 15)

    plt.imshow(np.split(grid_in, entries, 2)[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

    d_yeast_cells = cuda.to_device(yeast_cells)

    threads_per_block = (16, 16)
    blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # rng_states = create_xoroshiro128p_states(width * height * 10000, seed=1)

    for i in range(iterations):

        d_grid_in = cuda.to_device(grid_in)
        d_grid_out = cuda.to_device(np.zeros((width, height, entries), dtype=np.int32))
        rng_states = cuda.to_device(np.random.randint(0, 7, size=(width, height, entries, 10000), dtype=np.uint8))

        #rng_states = create_xoroshiro128p_states(threads_per_block[0] * blocks_per_grid_x, seed=i+1)

        diffusion_kernel[blocks_per_grid, threads_per_block](rng_states, d_grid_in, d_grid_out, d_yeast_cells)

        cuda.synchronize()

        res_grid_out = d_grid_out.copy_to_host()

        print("A")

        print(np.sum(res_grid_out))

        if i % 10 == 0:
            plt.imshow(np.split(res_grid_out, entries, 2)[0])
            plt.colorbar()
            plt.savefig(f"grid_post_{i}.jpg")
            plt.clf()

        grid_in = res_grid_out


if __name__ == "__main__":
    main()