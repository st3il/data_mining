__author__ = 'Jackdecrack'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from sklearn import cross_validation


dateiinhalt = pd.read_csv("data/effectiveRates.csv")

#print("effectiveRates");
#print(dateiinhalt);

cop = dateiinhalt[['COP', 'AXP', 'RTN', 'BA', 'AAPL']]




plt.plot(cop)
plt.title("Aktienkurse")
plt.show()



yahoo = dateiinhalt['YHOO']

print("Yahoo")
print(yahoo)
#print(len(cop))
#a = pd.np.array(dateiinhalt[[0]])
#a = a.flatten()
#print(list(a))
#print(len(a))


#time delay: 24  Anzahl der zu berucksichtigten vorhergehenden Kurswerte
#timeDelay = 24
timeDelay = 34

#Anlegen einer SVR  mit RBF Kernel (empfohlene Parameter: C = 500, epsilon = 0,6)
svrC = 500.0
#svrE = 0.6
svrE = 1.4 #optimaler Wert: 1,4


#
def createCyclicData(data):
    # Erzeuge Array in Form von Anzahl Werte x Anzahl der zu berucksichtigten vorhergehenden Kurswerte + heutiger Wert
    result = np.zeros((len(data),timeDelay+1))


    for i in range(len(data)):
        # hole Werte vom jwl vorhergehenden Tage
        for j in range(timeDelay+1):
            # calculate index of item
            index = i - (timeDelay-j)

            if index < 0:
                index = len(data) + index

            result[i,j] = data[index]

    return result



#Serielle Daten Yahoo
cycleTableYahoo = createCyclicData(yahoo)

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
plt.title("Yahoo Kurs")
plt.show()




#__________________________________________________________________________________________






# Erzeuge SVR
svr = SVR(C=svrC, epsilon=svrE, kernel='rbf')

# fitting
fittedData = svr.fit(features, targets)

# Vorhersagezeitraum
predictDuration = 30
predictedData = list()

for i in range(predictDuration):

    predictVector = np.zeros((timeDelay))

    # von 24 bis 0
    for j in range(timeDelay-1,-1, -1):

        idxPredict = len(predictedData)-j-1

        # unter null haben wir keine vorhergesagten Werte
        if idxPredict >= 0:
            predictVector[j] = predictedData[idxPredict]
            continue # could get value from predicted data -> use it!

        # hole bekannte Werte, wenn wir den Datenbvektro mit verhergesagten werten fuellen koennen
        idxTarget = 650 - j + len(predictedData)
        predictVector[j] = cycleTableYahoo[idxTarget, -1]

    predictedData.append(svr.predict(predictVector)[0])

# umwandeln in Array
predictedData = np.array(predictedData)

# print data from 651 -> 680
print "Predicted Data"
print predictedData
print "\nReal Values"
print targets[len(targets)-predictDuration:]

print "----------------------------MAE---------------------------------------"
# Berechne Mean Absolute Error
# MAE zeigt den mittleren Abweichwert

#reale Daten der letzten 30 Tage (predictDuration) :
compareRealYahooTargets = targets[len(targets)-predictDuration:]
mae = mean_absolute_error(compareRealYahooTargets, predictedData)

print "Mean Absolute Error:\t\t%0.3f" % mae

print "----------------------------PLOT---------------------------------------"
realForecast = cycleTableYahoo[649:(650+predictDuration), -1]
plt.plot(range(650,650+predictDuration),predictedData, '-r', label="prediction")
plt.plot(range(len(targets)), targets, '-k', label="real")
plt.plot(range(649, 650+predictDuration), realForecast, '-b', label="forecast")
plt.legend()
plt.show()