__author__ = 'Jackdecrack'


import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;



dateiinhalt = pd.read_csv("data/EnergyMix.csv")

dateiinhalt = dateiinhalt.set_index(dateiinhalt["Country"])
dateiinhalt = dateiinhalt.sort_index(axis=0, ascending=False);
dateiinhalt = dateiinhalt.drop("CO2Emm", 1)
dateiinhalt = dateiinhalt.drop("Total2009", 1)
dateiinhalt.plot(kind='bar', stacked=True)

plt.grid(True)



plt.show()