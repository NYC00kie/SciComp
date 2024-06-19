import sys
import matplotlib.pyplot as plt
import numpy as np

datenliste = [open(f"10-itterations-daten/params-{i}.csv", "r").readlines() for i in range(1,11)]

daten = datenliste[0]

for paramindex in range(6):
	for datenlisteindex in range(10):
		parami = np.array([float(data) for data in datenliste[datenlisteindex][paramindex].split(",")])
		plt.plot(parami,label=f"itt. {datenlisteindex}")

	plt.legend()
	plt.savefig(f"10-itterations-daten/cell_params_{paramindex}",dpi=800)
	plt.clf()
