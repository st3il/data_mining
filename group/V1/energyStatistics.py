import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### FUNCTIONS ###

def summaryChart(energyData):
    energyData = energyData.drop("Total2009",1)
    energyData = energyData.drop("CO2Emm",1)
    describe = energyData.describe()
    #describe.plot(kind="bar", stacked=True)
    #plt.show()

    for (i, item) in enumerate(describe):
        plt.subplot(5,1,i)
        describe.boxplot(column=[item],vert=False)
    plt.show()

### FUNCTIONS END ###


energyData = pd.read_csv("data/EnergyMix.csv")

summaryChart(energyData)