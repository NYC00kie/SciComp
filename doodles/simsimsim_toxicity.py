import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

"""# SIR

## statistical model
"""

n = 1000

beta = 0.01
gamma = 0.01
lam = 500000

dt = 1
t_max =100

times = np.arange(0,t_max,dt)

A = np.zeros(len(times))
C = np.zeros(len(times))
D = np.zeros(len(times))

A[0] = n

print(times)

# Doing the Statistical Model

print(len(times))

for i in range(len(times)-1):
  A[i+1] = A[i] + (- (beta/n * A[i] + (np.exp(np.sqrt(C[i]))*A[i])/(lam)))*dt
  C[i+1] = C[i] + (gamma * A[i]) * dt
  D[i+1] = D[i] + (beta/n * A[i] + ((np.exp(np.sqrt(C[i])))*A[i])/(lam)) * dt

plt.plot(times,A,label="A")
plt.plot(times,C,label="C")
plt.plot(times,D,label="D")

plt.legend()

plt.savefig("ACD-model.jpg")