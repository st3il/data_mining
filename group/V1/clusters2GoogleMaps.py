## IMPORT LIBRARIES ###
import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy.spatial.distance import *
from scipy.cluster.hierarchy import *
import pymaps

#load data from file
energyDataFrame = pd.read_csv("data/EnergyMixGeo.csv")

#get oil coal gas nuclear and hydro column
cleanedEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro', 'Total2009']]

#scale and put into dataframe
scaledEnergyData = pd.DataFrame(preprocessing.scale(cleanedEnergyDataFrame, axis=0, with_mean=False, with_std=True, copy=True))

#get distancematrix
distanceMatrix = pdist(scaledEnergyData,'correlation')

#get relative engerie usage
relEnergieUse = linkage(distanceMatrix, method='average')

clusterData = fcluster(relEnergieUse, 4, criterion="maxclust")

energyDataFrame['cluster'] = clusterData
energyDataFrame = np.array(energyDataFrame)
g = pymaps.PyMap()                         # creates an icon & map by default
icon1 = pymaps.Icon('icon1')               # create an additional icon
icon1.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
icon1.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
g.addicon(icon1)

icon2 = pymaps.Icon('icon2')               # create an additional icon
icon2.image = "http://labs.google.com/ridefinder/images/mm_20_red.png" # for testing only!
icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
g.addicon(icon2)

icon3 = pymaps.Icon('icon3')               # create an additional icon
icon3.image = "http://labs.google.com/ridefinder/images/mm_20_green.png" # for testing only!
icon3.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
g.addicon(icon3)

icon4 = pymaps.Icon('icon4')               # create an additional icon
icon4.image = "http://labs.google.com/ridefinder/images/mm_20_yellow.png" # for testing only!
icon4.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
g.addicon(icon4)

g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A" # you will get your own key
g.maps[0].zoom = 3

for (i, item) in enumerate(energyDataFrame):
    if(item[10] == 1):
        r = [item[8], item[9], item[0] + ": Oil: " + str(item[1]) + ": Coal: " + str(item[2]) + ": Gas: " + str(item[3]) + ": Nuclear: " + str(item[4]) + ": Hydro: " + str(item[5])+ ": Total2009: " + str(item[6]), 'icon1']
        g.maps[0].setpoint(r)
    if(item[10] == 2):
        r = [item[8], item[9], item[0] + ": Oil: " + str(item[1]) + ": Coal: " + str(item[2]) + ": Gas: " + str(item[3]) + ": Nuclear: " + str(item[4]) + ": Hydro: " + str(item[5])+ ": Total2009: " + str(item[6]), 'icon2']
        g.maps[0].setpoint(r)
    if(item[10] == 3):
        r = [item[8], item[9], item[0] + ": Oil: " + str(item[1]) + ": Coal: " + str(item[2]) + ": Gas: " + str(item[3]) + ": Nuclear: " + str(item[4]) + ": Hydro: " + str(item[5])+ ": Total2009: " + str(item[6]), 'icon3']
        g.maps[0].setpoint(r)
    if(item[10] == 4):
        r = [item[8], item[9], item[0] + ": Oil: " + str(item[1]) + ": Coal: " + str(item[2]) + ": Gas: " + str(item[3]) + ": Nuclear: " + str(item[4]) + ": Hydro: " + str(item[5])+ ": Total2009: " + str(item[6]), 'icon4']
        g.maps[0].setpoint(r)

#print g.showhtml()
open('test.htm','wb').write(g.showhtml())   # generate test file