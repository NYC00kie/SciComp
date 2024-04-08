import numpy as np
from KONSTANTS import *

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
	#

	U_max = cells[11][cellIdx]
	I = cells[14][cellIdx]
	Y = cells[15][cellIdx]


	# Nutriens Intake

	Field_Glucose = grid[0][cells[0][cellIdx],cells[1][cellIdx]]//1
	Field_Oxygen = grid[1][cells[0][cellIdx],cells[1][cellIdx]]//1
    Field_Ethanole = grid[2][cells[cellIdx][0],cells[cellIdx][1]]//1

	z_1 = np.random.normal(loc=U_max, scale=0.2*U_max)
    z_2 = np.random.normal(loc=cells[cellIdx][16], scale=0.2*cells[cellIdx][16])
    z_3 = np.random.normal(loc=cells[cellIdx][13], scale=0.2*cells[cellIdx][13])

	U = z_1 * np.pow(cells[cellIdx][3],2/3) * (1 - (cells[cellIdx][12] * cells[cellIdx][4]) - z_2 * Field_Glucose)

	Eaten = np.min((U,Field_Glucose))

	grid[0][cells[0][cellIdx],cells[1][cellIdx]] -= Eaten

	ME = I * cells[cellIdx][3] + Field_Ethanole * z_3 * np.pow(cells[cellIdx][3],2/3)

	if ME > Eaten:
		cells[10][cellIdx] += 1
		if cells[10][cellIdx] >= cells[9][cellIdx]:
			# The Cell has surpassed it maximum time without enough food.
			# It now has died
			for i in range(len(cells))
				cells[i][cellIdx] = 0

			return True;

	else:
		# The Cell has got enough food and can add to its mass
		delta_m = Y * (U - ME)
		cells[cellIdx] += delta_m

		# return ethanol if there was not enough oxygen to turn it all into water and CO_2
		if Field_Oxygen - 6*Eaten >= 0:
			# Perfect, the Oxygen cancelled out the Glucose, no Ethanol was produced
			# remove Oxygen
			grid[1][cells[0][cellIdx],cells[1][cellIdx]] += - 6 * Eaten
			# add CO_2
			grid[3][cells[0][cellIdx],cells[1][cellIdx]] += 6 * Eaten
		else:
			# Oh No, the Oxygen wasnt enough to compensate the Glucose.
			# How much Glucose was compensated ?
			not_compensated = (Eaten - Field_Oxygen*1/6)
			# for every glucose, 2 Ethanol will come from it
			grid[2][cells[0][cellIdx],cells[1][cellIdx]] = 2 * not_compensated

	return False

def reproduction(grid, cells, cellIdx):
	
    
    
	pass 


def do_cell(grid_name, cells_name, cellIdx):

	# load shared memory
	existing_shm_grid = shared_memory.SharedMemory(name=grid_name)
    grid = np.ndarray((4,width,height), dtype=np.float32, buffer=existing_shm_grid.buf)
    existing_shm_cells = shared_memory.SharedMemory(name=cells_name)
    cells = np.ndarray((4,width,height), dtype=np.float32, buffer=existing_shm_cells.buf)

    if metabolism(grid,cells,cellIdx):
    	return
