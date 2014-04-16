__author__ = 'Jackdecrack'

import pandas as pd;

import numpy as np;

import matplotlib.pyplot as plt;

import urllib, json, csv

#_DIRECTIONS_QUERY_URL = 'http://maps.googleapis.com/maps/api/directions/output?'

def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")[0].get("geometry").get("location")
    #A little ugly I concede, but I am open to all advices :) '''
    return info




dateiinhalt = pd.read_csv("data/EnergyMix.csv")


dateiinhalt.plot()


for i in dateiinhalt:
    if i!="Country":
        newC = pd.concat([dateiinhalt["Country"] , dateiinhalt[i]], axis=1)
        print(newC)
        newC = newC.set_index("Country")
        newC.plot();



        print("------------------------------")


print((dateiinhalt) );
#plt.show();



#Open the List file of adresses to look for corresponding lat and lng.

addresses = dateiinhalt["Country"]

#Loop to feed the func with adresses and output the lat & lng.
i=0
for a in addresses:
    i = i+1
    print(str(i) + ": " + str(a))

    r = geocode(a)
    print "%s %s" % (r['lat'], r['lng'])
