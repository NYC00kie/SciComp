from numba import cuda, vectorize, jit
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
import matplotlib.pyplot as plt
import math

@jit
def diffusion_normal(grid_in, grid_out, yeast_cells):
    height, width, entries = grid_in.shape

    for x in range(0,width):
        for y in range(0, height):
            for entri in range(entries):
                for item_num in range(grid_in[x, y, entri]):
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

                    

                    selected_neighbor = neighbor_indices[np.random.randint(0,7)]
                    grid_out[selected_neighbor[0], selected_neighbor[1], entri] += 1

                grid_in[x,y,entri] = 0

    return grid_in, grid_out


def main_cpu():
    width = 1000
    height = 1000
    cells_n = 10000
    iterations = 101

    entries = 1
    grid_in = np.random.randint(0, 800, size=(width, height, entries), dtype=np.uint16)
    grid_in[0, 0] = 10000

    grid_out = np.zeros((width, height, entries), dtype=np.uint16)

    yeast_cells = np.random.rand(cells_n, 15)

    plt.imshow(np.split(grid_in, entries, 2)[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

    for i in range(iterations):
        grid_in, grid_out = diffusion_normal(grid_in,grid_out,yeast_cells)

        print(grid_in)
        print(grid_out)

        if i % 10 == 0:
            plt.imshow(np.split(grid_out, entries, 2)[0])
            plt.colorbar()
            plt.savefig(f"grid_post_{i}.jpg")
            plt.clf()

        grid_out, grid_in = grid_in, grid_out


if __name__ == "__main__":
    main_cpu()
