import pandas as pd
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.svm import SVR
from sklearn import cross_validation
from scipy.cluster.hierarchy import *
from scipy.spatial.distance import *
import matplotlib.pyplot as plt
from sklearn import linear_model

#read energy csv
energyDataFrame = pd.read_csv("data/EnergyMix.csv")

#get oil coal gas nuclear and hydro column
featuredEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
targetEnergyDataFrame = energyDataFrame['CO2Emm']

linearKernel = SVR(kernel='linear', C=5.0, epsilon=0.10789)

tenValidate = cross_validation.KFold(len(featuredEnergyDataFrame), 10)

scores = cross_validation.cross_val_score(linearKernel, featuredEnergyDataFrame, targetEnergyDataFrame, scoring ="mean_squared_error", cv=10)

print "CrossValidation:"
print scores
print "\nCrossValidation Mean: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std()/2)

#start fitting
trainedData = linearKernel.fit(featuredEnergyDataFrame, targetEnergyDataFrame)

predictedData = linearKernel.predict(featuredEnergyDataFrame)

abs = predictedData - targetEnergyDataFrame
meanAbs = abs.mean();
if meanAbs < 0:
	meanAbs *= -1
print "\nMean Absolute: %0.3f" % (meanAbs)

print "\nSVR-Coefficients:"
print linearKernel.coef_

plt.plot(np.arange(len(featuredEnergyDataFrame)), predictedData, '-r', targetEnergyDataFrame, '-k')
plt.show()