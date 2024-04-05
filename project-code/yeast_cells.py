import numpy as np
from KONSTANTS import *

def Metabolism(grid,cell):
	#
	# U: aufgenommene Nahrungsmenge
	# z_1: Zufallsvariabel mit Mittelwert U_max und Standardabweichung 0.2 * U_max
	# c, K_1: Konstanten
	# U_max: Maximale Anzahl an Nahrungsteilchen pro Zeiteinheit und Oberflächeneinheit
	# I : Glukose pro Einheit Biomasse, die zum erhalt benötigt wird.
	#

	# Nutriens Intake

	Field_Glucose = grid[0][cell[0],cell[1]]//1

	z_1 = np.random.normal(loc=U_max, scale=0.2*U_max)

	U = z_1 * c * np.pow(cell[3],2/3) * (1 - (K_1 * cell[4]))

	Eaten = np.min((U,Field_Glucose))

	grid[0][cell[0],cell[1]] -= Eaten

	ME = I * cell[3] + K_2 * grid[2] * c * np.pow(cell[3],2/3)

	if ME < Eaten:
		
