__author__ = 'Jackdecrack'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from sklearn import cross_validation


dateiinhalt = pd.read_csv("src/effectiveRates.csv")

#print("effectiveRates");
#print(dateiinhalt);

cop = dateiinhalt[['COP', 'AXP', 'RTN', 'BA', 'AAPL']]

yahoo = dateiinhalt['YHOO']

print("Yahoo")
print(yahoo)
#print(len(cop))
#a = pd.np.array(dateiinhalt[[0]])
#a = a.flatten()
#print(list(a))
#print(len(a))


#time delay: 24  Anzahl der zu berucksichtigten vorhergehenden Kurswerte
timeDelay = 24
svrC = 500.0
svrE = 1.8


#
def createCyclicData(data, timeDelay):
    # create an array with the shape nrValues X timeDelay+Value
    result = np.zeros((len(data),timeDelay+1))

    # timedelay too small, return current data
    if timeDelay == 0:
        return data

    # go through each data-row
    for i in range(len(data)):
        #print "i:\t\t%d" % i

        # get the i-timeDelay values as input-attributes
        for j in range(timeDelay+1):
            # calculate index of item
            index = i - (timeDelay-j)

            # ring around the rosy
            if index < 0:
                index = len(data) + index

            #print "index:\t%d" % index

            # put value into result-index
            result[i,j] = data[index]

    return result



#Serielle Daten Yahoo
cycleTableYahoo = createCyclicData(yahoo, timeDelay)

print("cycleTableYahoo");
print( cycleTableYahoo)

print( len(cycleTableYahoo[0])) #--> ergibt timedelay plus 1 (aktueller tag)


# extract features and targets from data, use first 650 rows for training
features = np.array(cycleTableYahoo[:650,:timeDelay])
targets = cycleTableYahoo[:650, timeDelay:].reshape((650))

print( features)
print( len(features))









#plt.xticks(len(a), list(a))
plt.plot(yahoo)

plt.show()




#__________________________________________________________________________________________






# Create SVR with given settings
svr = SVR(C= svrC, epsilon= svrE, kernel='rbf')

print "----------------------------Fitting---------------------------------------"
# start fitting
fittedData = svr.fit(features, targets)

# data to predict: last 30 days
predictDuration = 30
predictedData = list()

print "----------------------------Prediction---------------------------------------"
for i in range(predictDuration):

    predictVector = np.zeros((timeDelay))
    # count from 23 to 0
    for j in range(timeDelay-1,-1, -1):
        # what is the index of the corresponding item in the predicted data?
        idxPredict = len(predictedData)-j-1

        # if we are below 0, it means we do not have any more predicted values
        if idxPredict >= 0:
            predictVector[j] = predictedData[idxPredict]
            #print "From predicted %f" % predictVector[j]
            continue # could get value from predicted data -> use it!

        # we could not fill the whole vector with already predicted data, fill it with already known data
        idxTarget = 650 - j + len(predictedData)
        predictVector[j] = cycleTableYahoo[idxTarget, -1]
       # print "From target %f" % predictVector[j]

    # predict the data using trainings-data from the SVR
    predictedData.append(svr.predict(predictVector)[0])

# stuff into a numpy array
predictedData = np.array(predictedData)

# print data from 651 -> 680
print "Predicted Data"
print predictedData
print "\nReal Values"
print targets[len(targets)-predictDuration:]

print "----------------------------MAD/MAE---------------------------------------"
# calculate the absolute deviation
mae = mean_absolute_error(targets[len(targets)-predictDuration:], predictedData)
mad = 1.0/predictDuration*np.sum(np.abs(predictedData-targets[len(targets)-predictDuration:]))

print "\nMean Absolute Deviation:\t%0.3f" % mad
print "Mean Absolute Error:\t\t%0.3f" % mae

print "----------------------------PLOT---------------------------------------"
# plot everything out
realForecast = cycleTableYahoo[649:(650+predictDuration), -1]
plt.plot(range(650,650+predictDuration),predictedData, '-r', label="prediction")
plt.plot(range(len(targets)), targets, '-k', label="real")
plt.plot(range(649, 650+predictDuration), realForecast, '-b', label="forecast")
plt.legend()
plt.show()