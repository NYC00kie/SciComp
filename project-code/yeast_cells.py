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

	U_max = cells[cellIdx][11]
	I = cells[cellIdx][14]
	Y = cells[cellIdx][15]


	# Nutriens Intake

	Field_Glucose = grid[0][cells[cellIdx][0],cells[cellIdx][1]]//1
	Field_Oxygen = grid[1][cells[cellIdx][0],cells[cellIdx][1]]//1
    Field_Ethanole = grid[2][cells[cellIdx][0],cells[cellIdx][1]]//1

	z_1 = np.random.normal(loc=U_max, scale=0.2*U_max)
    z_2 = np.random.normal(loc=cells[cellIdx][16], scale=0.2*cells[cellIdx][16])
    z_3 = np.random.normal(loc=cells[cellIdx][13], scale=0.2*cells[cellIdx][13])

	U = z_1 * np.pow(cells[cellIdx][3],2/3) * (1 - (cells[cellIdx][12] * cells[cellIdx][4]) - z_2 * Field_Glucose)

	Eaten = np.min((U,Field_Glucose))

	grid[0][cells[cellIdx][0],cells[cellIdx][1]] -= Eaten

	ME = I * cells[cellIdx][3] + Field_Ethanole * z_3 * np.pow(cells[cellIdx][3],2/3)

	if ME > Eaten:
		cells[cellIdx][10] += 1
		if cells[cellIdx][10] >= cells[cellIdx][9]:
			# The Cell has surpassed it maximum time without enough food.
			# It now has died
			for i in range(len(cells))
				cells[cellIdx][i] = 0

			return True;

	else:
		# The Cell has got enough food and can add to its mass
		delta_m = Y * (U - ME)
		cells[cellIdx][3] += delta_m

		# return ethanol if there was not enough oxygen to turn it all into water and CO_2
		if Field_Oxygen - 6*Eaten >= 0:
			# Perfect, the Oxygen cancelled out the Glucose, no Ethanol was produced
			# remove Oxygen
			grid[1][cells[cellIdx][0],cells[cellIdx][1]] += - 6 * Eaten
			# add CO_2
			grid[3][cells[cellIdx][0],cells[cellIdx][1]] += 6 * Eaten
		else:
			# Oh No, the Oxygen wasnt enough to compensate the Glucose.
			# How much Glucose was compensated ?
			not_compensated = (Eaten - Field_Oxygen*1/6)
			# for every glucose, 2 Ethanol will come from it
            # should be correct as we work with molecular amounts
			grid[2][cells[cellIdx][0],cells[cellIdx][1]] = 2 * not_compensated

	return False

def reproduction(grid, cells, cellIdx):
	#
	#
	#
	
	if cells[cellIdx][5] == 1:
		# Budding Phase 1

		delta_m = cells[cellIdx][3] - cells[cellIdx][6]
		if cells[cellIdx][7] <= delta_m:
			# cell reached minimal budding mass for phase 2
			cells[cellIdx][5] = 2

	else:
		# Budding Phase
		delta_m = cells[cellIdx][3] - cells[cellIdx][6]
		if 2 * cells[cellIdx][7] <= delta_m and cells[cellIdx][18] >= cells[cellIdx][8] :
			# Cell division requirements are met.
			# The time has come
			# Execute Order 66

			cells[cellIdx][3] += - delta_m

			cells[cellIdx][4] += 1

			babycell = [
			cells[0][cellIdx],
			cells[1][cellIdx],
			cells[2][cellIdx],
			delta_m,
			1,
			1,
			delta_m,
			cells[7][cellIdx],
			cells[8][cellIdx],
			cells[9][cellIdx],
			cells[10][cellIdx],
			cells[11][cellIdx],
			cells[12][cellIdx],
			cells[13][cellIdx],
			cells[14][cellIdx],
			cells[15][cellIdx],
			cells[16][cellIdx],
			0
			]

			cells.appen(babycell)

			return

		elif cells[cellIdx][18] <= cells[cellIdx][8]:
			# The Time has not come
			cells[cellIdx][18] += 1
			return

def spread_cell(grid,cells,cellIdx):
	pass

def do_cell(grid, cells, cellIdx):

	# load shared memory

    if metabolism(grid,cells,cellIdx):
    	return
    reproduction(grid,cells,cellIdx)
