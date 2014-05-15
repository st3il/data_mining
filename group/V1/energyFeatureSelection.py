import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression

### FUNCTIONS START ###

def featureSelection(energyDataFrame):
    #get oil coal gas nuclear and hydro column
    featuredEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    #get CO2Emm out of array
    targetEnergyDataFrame = energyDataFrame['CO2Emm']
    #feature selection with selectkbest function with scoring-function f_regression
    featureSelectin = SelectKBest(f_regression, 3)
    featureSelectin.fit(featuredEnergyDataFrame, targetEnergyDataFrame)
    #print results
    print featureSelectin.scores_

### FUNCTIONS END ###

#read file
energyDataFrame = pd.read_csv("data/EnergyMix.csv")

#call featureSelection function
featureSelection(energyDataFrame)



