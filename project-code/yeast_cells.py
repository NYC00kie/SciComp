import numpy as np
from KONSTANTS import *

def Metabolism(grid,cell):
	#
	# U: aufgenommene Nahrungsmenge
	# Z_1: Zufallsvariabel mit Mittelwert U_max und Standardabweichung 0.2 * U_max
	# c, k_1: Konstanten
	# U_max: Maximale Anzahl an Nahrungsteilchen pro Zeiteinheit und Oberflächeneinheit
	#

	U = 