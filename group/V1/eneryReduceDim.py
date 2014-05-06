## IMPORT LIBRARIES ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold


### FUNCTIONS START ###

def createIsomap(energyDataFrame):
    #get oil coal gas nuclear and hydro column
    cleanedEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    #get country column
    countrynames = np.array(energyDataFrame[['Country']])
    #get number of countries
    numOfInstances = len(countrynames)
    #create isomap
    imap = manifold.Isomap()
    #add data to isomap
    X = imap.fit_transform(cleanedEnergyDataFrame)
    #create plot
    plt.plot(X[:,0],X[:,1],'.')
    for z in range(numOfInstances):
        #add text
        plt.text(X[z,0], X[z,1], str(countrynames[z]))
    plt.show()

### FUNCTIONS END ###

#read file
energyDataFrame = pd.read_csv("data/EnergyMix.csv")

#createIsomap function call
createIsomap(energyDataFrame)

