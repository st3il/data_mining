import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy.cluster.hierarchy import *
from scipy.spatial.distance import *
import matplotlib.pyplot as plt

### FUNCTIONS START ####

def dendrogramClustering(energyDataFrame):
    #get country column
    countrynames = np.array(energyDataFrame[['Country']])

    #get oil coal gas nuclear and hydro column
    cleanedEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]

    #scale and put into dataframe
    scaledEnergyData = pd.DataFrame(preprocessing.scale(cleanedEnergyDataFrame, axis=0, with_mean=False, with_std=True, copy=True))

    #get distancematrix
    distanceMatrix = pdist(scaledEnergyData,'correlation')

    #get relative engerie usage
    relEnergieUse = linkage(distanceMatrix, method='average')

    #create dendrogram
    dendrogram(relEnergieUse, orientation='left',labels=countrynames)
    plt.show()

def singleClustering(energyDataFrame):
    #get oil coal gas nuclear and hydro column
    cleanedEnergyDataFrame = energyDataFrame[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]

    #scale and put into dataframe
    scaledEnergyData = pd.DataFrame(preprocessing.scale(cleanedEnergyDataFrame, axis=0, with_mean=False, with_std=True, copy=True))

    #get distancematrix
    distanceMatrix = pdist(scaledEnergyData,'correlation')

    #get relative engerie usage
    relEnergieUse = linkage(distanceMatrix, method='average')

    clusterData = fcluster(relEnergieUse, 4, criterion="maxclust")

    energyDataFrame['cluster'] = clusterData

    cluster1 = energyDataFrame[energyDataFrame['cluster'] == 1]
    cluster1 = cluster1[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    plt.subplot(411)
    plt.title('Cluster 1')
    plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
    plt.plot(cluster1.transpose())

    cluster2 = energyDataFrame[energyDataFrame['cluster'] == 2]
    cluster2 = cluster2[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    plt.subplot(412)
    plt.title('Cluster 2')
    plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
    plt.plot(cluster2.transpose())

    cluster3 = energyDataFrame[energyDataFrame['cluster'] == 3]
    cluster3 = cluster3[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    plt.subplot(413)
    plt.title('Cluster 3')
    plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
    plt.plot(cluster3.transpose())

    cluster4 = energyDataFrame[energyDataFrame['cluster'] == 4]
    cluster4 = cluster4[['Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro']]
    plt.subplot(414)
    plt.title('Cluster 4')
    plt.xticks(range(5), ('Oil', 'Coal', 'Gas', 'Nuclear', 'Hydro'))
    plt.plot(cluster4.transpose())

    plt.show()


### FUNCTIONS END ###

#read file
energyDataFrame = pd.read_csv("data/EnergyMix.csv")

#create dendromgram
#dendrogramClustering(energyDataFrame)

#create single cluster
singleClustering(energyDataFrame)

