__author__ = 'Jackdecrack'


import numpy as np
from sklearn import linear_model
from sklearn import metrics
from matplotlib import pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.svm import SVR



infileName='data/bodyfat.txt'
inp=open(infileName,'r')
plist=[];
for row in inp.readlines():
        k=row.split()
        u=[float(a) for a in k[1:]]     # convert and store columns 1-14
        plist.append(u)
numInstances=len(plist);

fullarray=np.array(plist)

fullarray.tofile('bodyfat_252_14',sep=',')
fa=np.fromfile('bodyfat_252_14',sep=',').reshape(numInstances,-1)

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

mse1=1.0/numInstances*np.sum((predictedOutput-targets)**2)
mse2=metrics.mean_squared_error(predictedOutput,targets);
mad1=1.0/numInstances*np.sum(np.abs(predictedOutput-targets))
mad2=1.0/numInstances*metrics.pairwise.manhattan_distances(predictedOutput,targets) #Same as MAD
print "Mean Squared Error 1 %2.3f" % (mse1)
print "Mean Squared Error 2 %2.3f" % (mse2)
print "Mean Absolute Difference 1 %2.3f" % (mad1)
print "Mean Absolute Difference 2 %2.3f" % (mad2)


print"\n\n##################### Approach 2: Simple partition in training- and testdataset ################"
# Split available dataset in disjoint training- and testdataset
numTrain=150;
training_features=features[:numTrain,:];
training_targets=targets[:numTrain];
test_features=features[numTrain:,:];
test_targets=targets[numTrain:];
# Choose Linear Regression
regressor2=linear_model.LinearRegression()
regressor2.fit(training_features,training_targets)      # Train the model using only the training data
# Output the learned coefficients of the linear model
print "Learned coefficients of the linear model:"
print regressor2.coef_
# Apply the learned linear model, i.e. input the test features and predict the corresponding outputs
predictedOutput = regressor2.predict(test_features)
Error2=predictedOutput-test_targets;
mse1=1.0/numInstances*np.sum((Error2)**2)
mad1=1.0/numInstances*np.sum(np.abs(Error2))
print "Mean Squared Error 1 \t %2.3f" % (mse1)
print "Mean Absolute Difference 1 \t %2.3f" % (mad1)


print"\n\n##################### Approach 3: 10-fold crossvalidation #################################"
regressor3=linear_model.LinearRegression()
print'----- Mean Square Error Score for Linear Regression------------'
scores = cross_val_score(regressor3,features,targets,cv=10,score_func=metrics.mean_squared_error)
print scores
print "Cross Validation Score: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() / 2)


print"\n\n############## Approach 4: SVM-Regression with 10-fold crossvalidation #########################"
regressor4=SVR(kernel='linear',C=1,epsilon=1.4)
print'----- Mean Square Error Score for SVM Regression ------------'
scores = cross_val_score(regressor4,features,targets,cv=10,score_func=metrics.mean_squared_error)
print scores
print "Cross Validation Score: %0.3f (+/- %0.3f)" % (scores.mean(), scores.std() / 2)