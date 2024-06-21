import multiprocessing
import sys

import numpy as np
from KONSTANTS import *
from numba import jit

grid = None

# @jit
def metabolism(cell):
    #
    # U: aufgenommene Nahrungsmenge
    # z_1: Zufallsvariabel mit Mittelwert U_max und Standardabweichung 0.2 * U_max
    # c, K_1: Konstanten
    # U_max: Maximale Anzahl an Nahrungsteilchen pro Zeiteinheit und Oberflächeneinheit
    # I : Glukose pro Einheit Biomasse, die zum erhalt benötigt wird.
    # Y: Metabolische Effizienz in Masse pro Glucose
    # E: esidual constant that accounts for the amount of residual product (ethanol) per unit of metabolized glucose particle
    #

    U_max = cell[11]
    I = cell[14]
    Y = cell[15]

    # Nutriens Intake

    Field_Glucose = grid[0][int(cell[0]), int(cell[1])]
    Field_Oxygen = grid[1][int(cell[0]), int(cell[1])]
    Field_Ethanole = grid[2][int(cell[0]), int(cell[1])]

    z_1 = np.random.normal(loc=U_max, scale=0.2 * U_max)
    z_2 = np.random.normal(loc=cell[16], scale=0.2 * cell[16])
    z_3 = np.random.normal(loc=cell[13], scale=0.2 * cell[13])
    U = z_1 * np.power(cell[3], 2 / 3) * (1 - (cell[12] * cell[4]) - z_2 * Field_Glucose)

    Eaten = min((U, Field_Glucose))

    # print( Eaten, z_2, Field_Glucose)

    ME = I * cell[3] + Field_Ethanole * z_3 * np.power(cell[3], 2 / 3)

    Difference = Eaten - ME

    # print(Difference, Eaten, ME)

    if Difference < 0:
        cell[10] += 1
        if cell[10] >= cell[9]:
            # The Cell has surpassed it maximum time without enough food.
            # It now has died
            cell[0] = 0
            cell[1] = 0
            cell[2] = 0
            cell[3] = 0
            cell[4] = 0
            cell[5] = 0
            cell[6] = 0
            cell[7] = 0
            cell[8] = 0
            cell[9] = 0
            cell[10] = 0
            cell[11] = 0
            cell[12] = 0
            cell[13] = 0
            cell[14] = 0
            cell[15] = 0
            cell[16] = 0
            cell[17] = 0
            cell[18] = 0

    else:
        grid[0][int(cell[0]), int(cell[1])] -= Eaten
        # The Cell has got enough food and can add to its mass
        delta_m = Y * Difference
        cell[3] += delta_m
        cell[10] = 0

        # return ethanol if there was not enough oxygen to turn it all into water and CO_2
        if Field_Oxygen - 2 * Eaten >= 0:
            # Perfect, the Oxygen cancelled out the Glucose, no Ethanol was produced
            # remove Oxygen
            grid[1][int(cell[0]), int(cell[1])] += -2 * Eaten
            # add CO_2
            grid[3][int(cell[0]), int(cell[1])] += 2 * Eaten
        else:
            # Oh No, the Oxygen wasnt enough to compensate the Glucose.
            # How much Glucose was compensated ?
            not_compensated = Eaten - Field_Oxygen * 1 / 2
            # for every glucose, 2 Ethanol will come from it
            # should be correct as we work with molecular amounts
            grid[2][int(cell[0]), int(cell[1])] += 2 * not_compensated


# @jit
def reproduction(cell):
    #
    #
    #

    # Hier war geplant, vom Modell aufgrund von Redundanz abzuweichen
    if cell[5] == 1:
        # cell cyclus phase 1: growing

        if cell[3] >= cell[6]:
            # if the current mass excedes the starting mass for phase 2
            cell[5] = 2

    else:
        delta_m = cell[3] - cell[6]

        if cell[7] <= delta_m and cell[17] >= cell[8]:
            # Cell division requirements are met.
            # The time has come
            # Execute Order 66

            cell[3] += -delta_m

            # aging
            cell[4] += 1
            cell[5] = 1

            babycell = [
                cell[0],
                cell[1],
                cell[2],
                delta_m,
                0,
                1,
                cell[6],
                cell[7],
                cell[8],
                cell[9],
                cell[10],
                cell[11],
                cell[12],
                cell[13],
                cell[14],
                cell[15],
                cell[16],
                0,
                delta_m,
            ]

            cell[6] += 0.1 * cell[3]

            #what do we want? An n Genen wird eine Mutation verursacht
            genes = np.array([6, 7, 8, 9, 11, 12, 13, 14, 15, 16])
            mutation_frequency = 2
            mutation = np.random.choice(genes, size = mutation_frequency)
            # print(mutation)
            for n in range(0, mutation_frequency):
                m_1 = np.random.normal(loc = 0, scale = 0.1*babycell[mutation[n]])
                babycell[mutation[n]] += m_1


            return babycell

        elif cell[17] <= cell[8]:
            # The Time has not come
            cell[17] += 1


# @jit
def spread_cell(cell):
    d_x, d_y = np.random.randint(-3, high=4, size=2)
    cell[0] = (cell[0] + d_x) % width
    cell[1] = (cell[1] + d_y) % height


# @jit
def do_cell(cell, dim):
    babycell = reproduction(cell)
    spread_cell(cell)
    metabolism(cell)
    # zelle stirbt, aber kommt lebendig wieder.

    return [cell] if babycell is None else [cell, babycell]
