# General
In here General Research informations will be placed like links to papers or other important Information

<https://academic.oup.com/jimb/article/35/11/1359/5993274?login=true>

<https://www.sciencedirect.com/science/article/pii/S0898122109005008>

# Scientific Ideas

Herstellung von Ethanol durch die alkoholische Gärung

Ethanol wird durch die alkoholische Gärung hergestellt. Bei der alkoholischen Gärung wandeln Hefepilze in sauerstoffarmer Umgebung Traubenzucker (Glucose) in Ethanol und Kohlenstoffdioxid Kohlenstoffdioxid
Kohlenstoffdioxid ist bekannt als.

und ein Bestandteil der Erdatmosphäre. Kohlenstoffdioxid entsteht bei der Verbrennung von kohlenstoffhaltigen Stoffen, also zum Beispiel wenn Holz verbrannt wird. um (Abb. 2).  

Bei dieser Reaktion wird Energie frei, es handelt sich also um eine exotherme Reaktion. Die Energie wird in den Hefezellen in Form von ATP gespeichert. ATP ist eine energiereiche Verbindung, die immer dann zum Einsatz kommt, wenn die Zelle Energie benötigt. Die Hefezellen nutzen die Energie für ihre Stoffwechselprozesse.

Damit die Hefezelle den Traubenzucker zu Alkohol und Wasser abbauen kann, benötigt die Hefezelle sogenannte Enzyme. Enzyme sind Eiweiße, die bestimmte Stoffwechselreaktionen ermöglichen. Die Enzyme wirken als Katalysatoren. Das bedeutet, dass die Enzyme die Aktivierungsenergie der Reaktion herabsetzen und dadurch die Reaktion beschleunigen.  

Die alkoholische Gärung ist von der Temperatur abhängig. Je höher die Temperatur, desto schneller verläuft die Gärung. Die Temperaturabhängigkeit kannst du z. B. bei einem Hefeteig beobachten. Stellst du den Teig an einen warmen Platz, dann „geht“ der Teig schneller. Ab ca.

werden jedoch die Enzyme in den Hefezellen zerstört (denaturiert) und der Gärprozess bricht ab.

Ethanol kann von den Hefezellen nicht weiterverarbeitet werden und wird als Abfallprodukt ausgeschieden. Dabei können Hefezellen nur einen Alkoholgehalt von maximal 19% vertragen, da Alkohol auch für Hefezellen – wie für menschliche Zellen – giftig ist. Bei einem höheren Alkoholgehalt sterben die Hefezellen ab.

# Ideas

Die Aktuelle Idee für den Code ist:

in einem Grid :

- Hefe
- Glucose
- Sauerstoff

Werden zu 

- Hefe
- Ethanol
- CO_2


Diffusion wird über faltung mit einem kernel gelöst

# Code Conventions

Glucose grid ist Index 0
Sauerstoff grid ist Index 1
Ethanol grid ist Index 2
CO_2 grid ist Index 3

Cell indices:
0: x
1: y
2: z
3: mass
4: genealogical age
5: reproduction phase
6: start masse
7: minimum growth of biomass for the initiation of the budding phase
8: the minimum time required to complete the budding phase
9: its survival time without satisfying its metabolic requirements.
10: Mortalitätsindex
11: Maximal mögliche Zahl an konsumierter Nahrung pro Zeit und Oberfläche
12: Altersschwäche (Narbenbedingt)
13: Ethanolinhibition
14: Überlebensrelevante Nahrungsmenge in Glucose in mol pro Masseneinheit
15: Metabolische Effizienz in Masse pro Glucose
16: Glucoseinhibition
17: time in budding phase
