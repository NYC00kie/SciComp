#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
p = 0.1

n = 1000

adjacency_Matrix = np.matrix([[0, 1, 0, 1],
                              [1, 0, 1, 1],
                              [0, 1, 0, 1],
                              [0, 0, 0, 0]])


adjacency_Matrix = np.zeros([n,n],dtype=np.float16)

random.seed(1)

for i,row in enumerate(adjacency_Matrix):
  for j,element in enumerate(row):
    if j >= i: continue;
    if random.random() <= p:
      adjacency_Matrix[i][j] = 1

transposed = adjacency_Matrix.transpose()

adjacency_Matrix = np.add(adjacency_Matrix,transposed)

print(adjacency_Matrix)
print(transposed)

G = nx.from_numpy_array(adjacency_Matrix)


nx.draw_circular(G)

plt.savefig("test.jpg")
plt.close()

"""# SIR

## statistical model
"""

n = 100000

beta = 0.5
gamma = 0.04

dt = 0.1

times = np.arange(0,100,dt)

S = np.zeros(len(times))
I = np.zeros(len(times))
R = np.zeros(len(times))

S[0] = n
I[0] = 1

print(times)

# Doing the Statistical Model

print(len(times))

for i in range(len(times)-1):
  S[i+1] = S[i] + (- beta * S[i] * I[i] / n)*dt
  I[i+1] = I[i] + ((beta * S[i] * I[i] / n) - gamma * I[i] ) * dt
  R[i+1] = R[i] + (gamma * I[i]) * dt

plt.plot(times,S)
plt.plot(times,I)
plt.plot(times,R)

plt.savefig("test2.jpg")

"""# SIR Probabilistic modell"""

n = 0

People = np.zeros(n)