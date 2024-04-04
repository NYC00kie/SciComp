from numba import cuda, vectorize, jit
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
import matplotlib.pyplot as plt
import math
# from multiprocessing import Process, Queue
from multiprocessing import shared_memory, Process, Lock
from multiprocessing import cpu_count, current_process
import copy

def create_shared_block(dim):

    a = np.zeros(dim, dtype=np.uint32)  # Start with an existing NumPy array

    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
    # # Now create a NumPy array backed by shared memory
    np_array = np.ndarray(a.shape, dtype=np.uint32, buffer=shm.buf)
    np_array[:] = a[:]  # Copy the original data into shared memory
    return shm, np_array


@jit
def diffusing(rng_states, grid_in, grid_out, dim, entri):
    entries, height, width = dim

    for x in range(0,width):
        for y in range(0, height):      
            for item_num in range(grid_in[entri,x, y]):
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

                

                selected_neighbor = neighbor_indices[rng_states[entri,x,y, item_num]]
                grid_out[entri, selected_neighbor[0], selected_neighbor[1]] += 1



def diffusion_normal(rng_states, grid_in, shr_name, dim, entri):

    # creating the shared memory buffer
    existing_shm = shared_memory.SharedMemory(name=shr_name)
    grid_out = np.ndarray(dim, dtype=np.uint32, buffer=existing_shm.buf)

    diffusing(rng_states, grid_in, grid_out, dim, entri)

    existing_shm.close()

def main_cpu():
    width = 100
    height = 100

    cells_n = 10000
    iterations = 11
    entries = 4

    dim = (entries,width,height)
    
    grid_in = np.random.randint(0, 800, size=dim, dtype=np.uint16)

    yeast_cells = np.random.rand(cells_n, 15)

    plt.imshow(grid_in[0])
    plt.colorbar()
    plt.savefig("grid_pre.jpg")
    plt.clf()

    for i in range(iterations):
        rng_states = np.random.randint(0, 7, size=(entries, width, height, 10000), dtype=np.uint8)
        shr, grid_out = create_shared_block(dim)

        processes = []
        for entri in range(entries):
            _process = Process(target=diffusion_normal, args=(rng_states,grid_in,shr.name,dim,entri,))
            processes.append(_process)
            _process.start()

        for _process in processes:
            _process.join()
            print("one more done")

        print(np.sum(grid_out))

        for entri in range(entries):

            if i % 10 == 0:
                plt.imshow(grid_out[entri])
                plt.colorbar()
                plt.savefig(f"grid_post_{entri}_{i}.jpg")
                plt.clf()

        grid_in = copy.deepcopy(grid_out)

        # delete the old memory
        shr.close()
        shr.unlink()



if __name__ == "__main__":
    lock = Lock()

    main_cpu()
