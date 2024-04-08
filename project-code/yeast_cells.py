import numpy as np
from KONSTANTS import *

def Metabolism(grid,cells,cellIdx):
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
	U_max = cells[cellIdx][11]
	I = cells[cellIdx][14]
	Y = cells[cellIdx][15]


	# Nutriens Intake

	Field_Glucose = grid[0][cells[cellIdx][0],cells[cellIdx][1]]//1
	Field_Oxygen = grid[1][cells[cellIdx][0],cells[cellIdx][1]]//1

	z_1 = np.random.normal(loc=U_max, scale=0.2*U_max)

	U = z_1 * c * np.pow(cells[cellIdx][3],2/3) * (1 - (K_1 * cells[cellIdx][4]))

	Eaten = np.min((U,Field_Glucose))

	grid[0][cells[cellIdx][0],cells[cellIdx][1]] -= Eaten

	ME = I * cells[cellIdx][3] + K_2 * grid[2][cells[cellIdx][0],cells[cellIdx][1]] * c * np.pow(cells[cellIdx][3],2/3)

	if ME > Eaten:
		cells[cellIdx][16] += 1
		if cells[cellIdx][16] >= cells[cellIdx][9]:
			# The Cell has surpassed it maximum time without enough food.
			# It now has died
			cells[cellIdx] = np.zeros(len(cells[cellIdx]))
			return;

	else:
		# The Cell has got enough food and can add to its mass
		delta_m = Y * (U - ME)
		cells[cellIdx] += delta_m

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
			grid[2][cells[cellIdx][0],cells[cellIdx][1]] = 2 * not_compensated