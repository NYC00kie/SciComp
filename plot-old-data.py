import sys
import matplotlib.pyplot as plt
import matplotlib.colors as color
import matplotlib.cm as cm
import numpy as np
import scipy

length = 10

norm = color.Normalize(vmin=0, vmax=length+2)
cmap = cm.hsv
m = cm.ScalarMappable(norm=norm, cmap=cmap)

datenliste = [open(f"new-20-calcs/params-{i}.csv", "r").readlines() for i in range(1,length+1)]

daten = datenliste[0]

for paramindex in range(6):
	for datenlisteindex in range(length):

		parami = np.array([float(data) for data in datenliste[datenlisteindex][paramindex].split(",")])
		line, = plt.plot(np.arange(len(parami)),parami,label=f"itt. {datenlisteindex}")
		line.set_color(m.to_rgba(datenlisteindex))

	plt.legend()
	plt.savefig(f"new-20-calcs/cell_params_{paramindex}",dpi=800)
	plt.clf()
