import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib, json, csv
import time

_DIRECTIONS_QUERY_URL = 'http://maps.googleapis.com/maps/api/directions/output?'

def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")[0].get("geometry").get("location")
    #A little ugly I concede, but I am open to all advices :) '''
    return info

energyData = pd.read_csv("data/EnergyMix.csv")

#print energyData
#print '\n'
for (i, row) in enumerate(energyData):
    #print energyData['Country']

    if row !='Country':
        rowData = pd.concat([energyData['Country'], energyData[row]], axis=1)

        rowData = rowData.set_index('Country')

        rowData = rowData.sort_index(axis=0, ascending=True)
        #print rowData
        #plt.subplot(2,4,i)
        #rowData[row].plot()
        #plt.title(row)

#plt.show()

#Loop to feed the func with adresses and output the lat & lng.
for (i, country) in enumerate(energyData['Country']):
    if i%5 == 0:
        time.sleep(2)
    r = geocode(country)

    print str(country)
    print " %s %s" % (r['lat'], r['lng'])