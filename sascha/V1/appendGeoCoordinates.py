import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib, json, csv
import time

_DIRECTIONS_QUERY_URL = 'http://maps.googleapis.com/maps/api/directions/output?'

### functions ###
def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")[0].get("geometry").get("location")
    return info


def getCoordinatesForCountries(countries):
    for (i, country) in enumerate(countries):
        if i%5 == 0:
            time.sleep(2)
        r = geocode(country)

        print str(country)+" %s %s" % (r['lat'], r['lng'])


def getCountryCoordinates(county,j):
        r = geocode(county)
        if j%5 == 0:
            time.sleep(2)
        return [r['lat'],r['lng']]


def plotCharts(energyData):
    for (i, row) in enumerate(energyData):
        if row !='Country':
            rowData = pd.concat([energyData['Country'], energyData[row]], axis=1)
            rowData = rowData.set_index('Country')
            rowData = rowData.sort_index(axis=0, ascending=True)
            plt.subplot(2,4,i)
            rowData[row].plot()
            plt.title(row)

    plt.show()


def appendGeoToCountries(energyData):
    df = pd.DataFrame(columns=["Country","Lat","Long"])
    for (i, row) in enumerate(energyData):
        if row =='Country':
            for (j, country) in enumerate(energyData[row]):
                coordinates = getCountryCoordinates(country,j)
                print coordinates
                df.loc[j] = [country,coordinates[0],coordinates[1]]
    nf = pd.merge(energyData, df, on='Country', how='outer')
    nf = nf.set_index('Country')
    nf.to_csv('data/EnergyMixGeo.csv')

### functions end ###

energyData = pd.read_csv("data/EnergyMix.csv")

# show charts of coutry statistics
#plotCharts(energyData)

#show geo-coordinates of contries
#getCountryCoordinates(energyData['Country'])

#append geo coordinates to new file
appendGeoToCountries(energyData)








