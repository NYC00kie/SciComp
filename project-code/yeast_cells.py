import numpy as np
from numba import jit
from KONSTANTS import *
import sys


@jit
def metabolism(grid,cells,cellIdx):
    #
    # U: aufgenommene Nahrungsmenge
    # z_1: Zufallsvariabel mit Mittelwert U_max und Standardabweichung 0.2 * U_max
    # c, K_1: Konstanten
    # U_max: Maximale Anzahl an Nahrungsteilchen pro Zeiteinheit und Oberflächeneinheit
    # I : Glukose pro Einheit Biomasse, die zum erhalt benötigt wird.
    # Y: Metabolische Effizienz in Masse pro Glucose
    # E: esidual constant that accounts for the amount of residual product (ethanol) per unit of metabolized glucose particle
    #

    U_max = cells[cellIdx][11]
    I = cells[cellIdx][14]
    Y = cells[cellIdx][15]


    # Nutriens Intake

    Field_Glucose = grid[0][int(cells[cellIdx][0]),int(cells[cellIdx][1])]
    Field_Oxygen = grid[1][int(cells[cellIdx][0]),int(cells[cellIdx][1])]
    Field_Ethanole = grid[2][int(cells[cellIdx][0]),int(cells[cellIdx][1])]

    z_1 = np.random.normal(loc=U_max, scale=0.2*U_max)
    z_2 = np.random.normal(loc=cells[cellIdx][16], scale=0.2*cells[cellIdx][16])
    z_3 = np.random.normal(loc=cells[cellIdx][13], scale=0.2*cells[cellIdx][13])
    U = z_1 * np.power(cells[cellIdx][3],2/3) * (1 - (cells[cellIdx][12] * cells[cellIdx][4]) - z_2 * Field_Glucose)

    Eaten = min((U,Field_Glucose))

    grid[0][int(cells[cellIdx][0]),int(cells[cellIdx][1])] -= Eaten

    ME = I * cells[cellIdx][3] + Field_Ethanole * z_3 * np.power(cells[cellIdx][3],2/3)


    Difference = Eaten - ME

    # print(Difference, Eaten, ME)

    if Difference < 0:
        cells[cellIdx][10] += 1
        if cells[cellIdx][10] >= cells[cellIdx][9]:
            # The Cell has surpassed it maximum time without enough food.
            # It now has died
            cells[cellIdx] = np.zeros(cell_parameters)

    else:
        # The Cell has got enough food and can add to its mass
        delta_m = Y * Difference

        cells[cellIdx][3] += delta_m
        cells[cellIdx][10] = 0

        # return ethanol if there was not enough oxygen to turn it all into water and CO_2
        if Field_Oxygen - 6*Eaten >= 0:
            # Perfect, the Oxygen cancelled out the Glucose, no Ethanol was produced
            # remove Oxygen
            grid[1][int(cells[cellIdx][0]),int(cells[cellIdx][1])] += - 6 * Eaten
            # add CO_2
            grid[3][int(cells[cellIdx][0]),int(cells[cellIdx][1])] += 6 * Eaten
        else:
            # Oh No, the Oxygen wasnt enough to compensate the Glucose.
            # How much Glucose was compensated ?
            not_compensated = (Eaten - Field_Oxygen*1/6)
            # for every glucose, 2 Ethanol will come from it
            # should be correct as we work with molecular amounts
            grid[2][int(cells[cellIdx][0]),int(cells[cellIdx][1])] = 2 * not_compensated


@jit
def reproduction(grid, cells, cellIdx):
    #
    #
    #
         
    # Hier war geplant, vom Modell aufgrund von Redundanz abzuweichen
    if cells[cellIdx][5] == 1:
        # cell cyclus phase 1: growing
        if cells[cellIdx][3] >= cells[cellIdx][6]:
            #if the current mass excedes the starting mass for phase 2
            cells[cellIdx][5] = 2
    

    else:
        
        delta_m = cells[cellIdx][3] - cells[cellIdx][6]
        if cells[cellIdx][7] <= delta_m and cells[cellIdx][17] >= cells[cellIdx][8] :
            # Cell division requirements are met.
            # The time has come
            # Execute Order 66

            cells[cellIdx][3] += - delta_m
            
            # aging
            cells[cellIdx][4] += 1
            cells[cellIdx][5] = 1

            babycell = np.array([[
                                    cells[cellIdx][0],
                                    cells[cellIdx][1],
                                    cells[cellIdx][2],
                                    delta_m,
                                    0,
                                    1,
                                    cells[cellIdx][6],
                                    cells[cellIdx][7],
                                    cells[cellIdx][8],
                                    cells[cellIdx][9],
                                    cells[cellIdx][10],
                                    cells[cellIdx][11],
                                    cells[cellIdx][12],
                                    cells[cellIdx][13],
                                    cells[cellIdx][14],
                                    cells[cellIdx][15],
                                    cells[cellIdx][16],
                                    0,
                                    delta_m
                                    ]])

            cells[cellIdx][6] += 0.1 * cells[cellIdx][3]
            
            #what do we want? An n Genen wird eine Mutation verursacht
            genes = np.array([6, 7, 8, 9, 11, 12, 13, 14, 15, 16])
            mutation_frequency = 2
            mutation = np.random.choice(genes, size = mutation_frequency)
            # print(mutation)
            for n in range(0, mutation_frequency):
                m_1 = np.random.normal(loc = 0, scale = 0.1*cells[cellIdx][mutation[n]])
                cells[cellIdx][mutation[n]] += m_1
                
            cells = np.append(cells, babycell, axis=0)

        elif cells[cellIdx][17] <= cells[cellIdx][8]:
            # The Time has not come
            cells[cellIdx][17] += 1

    return cells

#@jit
def spread_cell(grid,cells,cellIdx):

    d_x,d_y = np.random.randint(-3,high=4, size=2)
    cells[cellIdx][0] = (cells[cellIdx][0] + d_x) % width
    cells[cellIdx][1] = (cells[cellIdx][1] + d_y) % height

#@jit
def do_cell(grid, cells, cellIdx):

    cells = reproduction(grid,cells,cellIdx)
    spread_cell(grid,cells,cellIdx)
    metabolism(grid,cells,cellIdx)

    return cells
