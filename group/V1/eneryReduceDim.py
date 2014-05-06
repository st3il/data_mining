import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
### FUNCTIONS START ###

def createIsomap(energyDataFrame):
    cleanedEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    countrynames = np.array(energyDataFrame[['Country']])

    countrynames = countrynames[:]

    numOfInstances = len(countrynames)

    imap = manifold.Isomap()

    X = imap.fit_transform(cleanedEnergyDataFrame)

    plt.plot(X[:,0],X[:,1],'.')
    for z in range(numOfInstances):
        plt.text(X[z,0], X[z,1], str(countrynames[z]))
    plt.show()

### FUNCTIONS END ###

#read file
energyDataFrame = pd.read_csv("data/EnergyMix.csv")

createIsomap(energyDataFrame)

