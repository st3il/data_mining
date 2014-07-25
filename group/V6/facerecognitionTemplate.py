from os.path import isdir,join,normpath
from os import listdir

#Tobi und Chen brauchen das:
#import Image
#Sascha braucht das:
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import asfarray,dot,argmin,zeros
from numpy import average,sort,trace, argsort
from numpy.linalg import svd,eigh
from numpy import concatenate, reshape
import tkFileDialog

def parseDirectory(directoryName,extension):
    '''This method returns a list of all filenames in the Directory directoryName. 
    For each file the complete absolute path is given in a normalized manner (with 
    double backslashes). Moreover only files with the specified extension are returned in 
    the list.
    '''
    if not isdir(directoryName): return
    imagefilenameslist=sorted([
        normpath(join(directoryName, fname))
        for fname in listdir(directoryName)
        if fname.lower().endswith('.'+extension)            
        ])
    return imagefilenameslist

#####################################################################################
# Implement required functions here
#
#
#
def generateListOfImgs(listOfTrainFiles):
    # Liste mit Bilder
    listOfImage = []

    #speichter Images
    for file in listOfTrainFiles:
        #oeffne Datei
        image = Image.open(file)
        # erzeuge graues bild
        image = image.convert('L')
        listOfImage.append(image)

    return listOfImage

def createImgAsNumpyData(img):
    imglist = list()
    imglist.append(img)

    numpyList = convertImageListToNumpyData(imglist)
    return numpyList[0]


def convertImageListToNumpyData(imgList):
    # konvertiere Bilder in ein numpy array 0
    # erzeuge die Matrix : Pixelanzahl(33000) x Bildanzahhl
    # bestimme hochsten Wert fur Normierung
    # Normiere Pixelwerte zwischen 1 und 0

    #numpaArray = np.array(imgList[x] for x in imgList)
    imgArrays = list()
    for img in imgList:
        npArray = asfarray(img)

        npArray = npArray.reshape(1, img.size[0]*img.size[1])

        # normierung:
        maxV = npArray.max()

        npArray = npArray/maxV

        imgArrays.append(npArray)

    return concatenate(imgArrays, axis=0)

def removeAverageOfImage(normedArray, averageArray):
    copyArray = normedArray.copy()

    for image in copyArray:
        image -= averageArray

    return copyArray


def calculateEigenfaces(adjfaces, width, height):
    #CV
    CV = dot(adjfaces, adjfaces.transpose())

    #Eigenwerte:
    eigenValues, eigenVectors = eigh(CV)

    # sortierung
    sortI = argsort(eigenValues)[::-1]
    eigenValues = eigenValues[sortI]
    eigenVectors = eigenVectors[sortI]

    # calculate Eigenfaces from Eigenvectors
    eigenfaces = dot(adjfaces.transpose(), eigenVectors).transpose()

    # restrict to K faces
    return eigenfaces[:6]

def calcEigenfaceCoord(NormedArrayOfFaces, Usub):

    shapedNormedArrayOfFaces = NormedArrayOfFaces.shape[0]
    shapedUsub = Usub.shape[0]

    EigenFaceCoord = np.zeros((shapedUsub, shapedNormedArrayOfFaces))

    for i in range(shapedNormedArrayOfFaces):
        for k in range(shapedUsub):

            #Berechnung Eigenfacekoordinaten und multipliziere mit Eigenvektor
            EigenFaceCoord[k, i] = dot(Usub[k, :], NormedArrayOfFaces[i, :])

    return EigenFaceCoord.transpose()

def calcEigenfaceCoordforTestImage(NormedTestBild, Usub):

    TestfaceCoordinates = np.zeros((Usub.shape[0])) #calculateEigenfaceCoordinates(NormedTestFace, Usub)

    # go through each of the eigenvectors of the eigenface
    for k in range(Usub.shape[0]):
        # calculate eingeface-coordinate of that image by multiplying it with the eigenvector
        TestfaceCoordinates[k] = dot(Usub[k,:], NormedTestBild)

    return TestfaceCoordinates

def euclideanDist(A, B):
    return np.linalg.norm(A-B)

def getNearestImage(TestfaceCoords, EigenfaceCoords):
    dist = sys.float_info.max
    closestImaId = 0
    for id, faceCoords in enumerate(EigenfaceCoords):
        newDist = euclideanDist(TestfaceCoords, faceCoords)
        if dist > newDist:
            closestImaId = id
            dist = newDist

    return closestImaId, dist

####################################################################################
#Start of main programm

#Choose Directory which contains all training images 
TrainDir=tkFileDialog.askdirectory(title="Choose Directory of training images")
#Choose the file extension of the image files
Extension='png'
#Choose the image which shall be recognized
testImageDirAndFilename=tkFileDialog.askopenfilename(title="Choose Image to detect")

####################################################################################
# Implement required functionality of the main programm here

imageFiles = parseDirectory('training', 'png')
#print('Alle Trainingsbilder:')
#print(imageFiles)

images = generateListOfImgs(imageFiles)

#print("Kontrolliere B und H")

width = 167
height = 250

# for image in images:
#     #print('Breite %d' %image.size[0])
#     width = image.size[0]
#     #print('Hoehe %d' %image.size[1])
#     height = image.size[1]
#     #break



# konvertiere Bilder in Zahlen
floatFaces = convertImageListToNumpyData(images)

# das Durchschnittsbild in Zahlen
averageFace = np.average(floatFaces, axis=0)

# Bilder ohne Durchschnittsbild in Zahlen
NormedArrayOfFaces = removeAverageOfImage(floatFaces, averageFace)

#print(NormedArrayOfFaces)

Usub = calculateEigenfaces(NormedArrayOfFaces, width,height)

#print(Usub)

## Zeige Eigenfaces
# eigenFaceImage = plt.figure()
# for i in range(Usub.shape[0]):
#     image = Usub[i,:]
#     imageCopy = np.reshape(image, (height, width))
#     axe = eigenFaceImage.add_subplot(2,3,i)
#     axe.xaxis.set_visible(False)
#     axe.yaxis.set_visible(False)
#     axe.imshow(imageCopy, cmap = plt.cm.gray)
#
# plt.show()

testBild = Image.open(testImageDirAndFilename)
testBild = testBild.convert('L')

testBildNumpy = createImgAsNumpyData(testBild)

NormedTestBild = removeAverageOfImage(np.array(testBildNumpy), averageFace)

EigenfaceCoordinates = calcEigenfaceCoord(NormedArrayOfFaces, Usub)

TestfaceCoordinates = calcEigenfaceCoordforTestImage(NormedTestBild, Usub)

NearestImageIndex, dist = getNearestImage(TestfaceCoordinates, EigenfaceCoordinates)

### zeige alle Eigenfaces
resultFig = plt.figure()
resultFig.suptitle("Euclid Distanz %.3f" % (dist))

ax = resultFig.add_subplot(1,2,1)
ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
ax.imshow(testBild, cmap=plt.cm.gray)

ax2 = resultFig.add_subplot(1,2,2)
ax2.yaxis.set_visible(False)
ax2.xaxis.set_visible(False)
ax2.imshow(images[NearestImageIndex], cmap=plt.cm.gray)

plt.show()