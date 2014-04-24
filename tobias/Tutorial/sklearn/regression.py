import numpy as np
from sklearn import linear_model
from sklearn import metrics
from matplotlib import pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.svm import SVR

infileName = 'data/bodyfat.txt'

inp = open(infileName, 'r')
plist=[];
for row in inp.readlines():
        k=row.split()
        u=[float(a) for a in k[1:]]     # convert and store columns 1-14
        plist.append(u)
numInstances=len(plist);

fullarray=np.array(plist)

fullarray.tofile('data/export/bodyfat_252_14',sep=',')
fa=np.fromfile('data/export/bodyfat_252_14',sep=',').reshape(numInstances,-1)

features=fa[:,1:]
targets=fa[:,0]

regressor=linear_model.LinearRegression()
regressor.fit(features,targets)         # Train the model using all available data

print regressor.coef_
print regressor.intercept_

predictedOutput = regressor.predict(features)
Error=predictedOutput-targets
plt.stem(np.arange(numInstances),Error)
plt.title('Prediction Error')
plt.show()