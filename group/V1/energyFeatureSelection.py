import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, chi2
from scipy.cluster.hierarchy import *
from scipy.spatial.distance import *
import matplotlib.pyplot as plt
from sklearn import linear_model

#read energy csv
energyDataFrame = pd.read_csv("data/EnergyMix.csv")

#get oil coal gas nuclear and hydro column
featuredEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
targetEnergyDataFrame = energyDataFrame['CO2Emm']

regressor = linear_model.LinearRegression()
regressor.fit(featuredEnergyDataFrame,targetEnergyDataFrame)

ch2 = SelectKBest(chi2, k=1)

ch2.fit(featuredEnergyDataFrame, targetEnergyDataFrame)

print ch2.scores_

