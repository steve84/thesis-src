# -*- coding: utf-8 -*-
import numpy as np
import csv

from sklearn import neighbors, linear_model, svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error
from scipy import stats
from random import sample

def kNNRegression(training_data, training_labels, testing_data, testing_labels, params={'n_neighbors': [1, 3, 5]}, cv=5):
		# initialise k-fold cross-validation grid search
    clf = GridSearchCV(neighbors.KNeighborsRegressor(), params, cv=cv)
    clf.fit(training_data, training_labels)
		# train the kNN		
    knn = neighbors.KNeighborsRegressor(n_neighbors=clf.best_estimator_.n_neighbors).fit(training_data, training_labels)
		# predict the results of the test data
    results = knn.predict(testing_data)
		# evaluate the results
    mse = mean_squared_error(testing_labels, results)
    return knn, results, mse
    
def SVRegression(training_data, training_labels, testing_data, testing_labels, params={'C':[1, 5, 10]}, cv=5):
		# initialise k-fold cross-validation grid search
    clf = GridSearchCV(svm.SVR(), params, cv=cv)
    clf.fit(training_data, training_labels)
		# train the support vector machine
    svr = svm.SVR(kernel=clf.best_estimator_.kernel, C=clf.best_estimator_.C).fit(training_data, training_labels)
    results = svr.predict(testing_data)
		# evaluate the results
    mse = mean_squared_error(testing_labels, results)
    return svr, results, mse
    
def RandomTreeRegression(training_data, training_labels, testing_data, testing_labels, n_estimators=10):
		# train the random forest tree
    rfc = RandomForestRegressor(n_estimators=n_estimators).fit(training_data, training_labels)
		# predict the results of the test data		
    results = rfc.predict(testing_data)
		# evaluate the results
    mse = mean_squared_error(testing_labels, results)
    return rfc, results, mse
    
def ParamsRandomTreeRegression(training_data, training_labels, params={'n_estimators':[1, 5, 10]}, cv=5):
		# initialise k-fold cross-validation grid search
    clf = GridSearchCV(RandomForestRegressor(), params, cv=cv)
    clf.fit(training_data, training_labels)
    return clf.best_estimator_.n_estimators
    
fname = '../../../../../training_data/playstation/train/trainingDataNormalized.csv'

reader = csv.reader(open(fname,"rb"),delimiter='\t')
next(reader)
x = list(reader)
data = np.array(x).astype('float')

training_labels = data[:,-1]
training_data = data[:,0:-1]

fname = '../../../../../training_data/playstation/test/testDataNormalized.csv'

reader = csv.reader(open(fname,"rb"),delimiter='\t')
next(reader)
x = list(reader)
data = np.array(x).astype('float')

testing_labels = data[:,-1]
testing_data = data[:,0:-1]

# grid search parameters of the machine learning algorithms
params_knn = {'n_neighbors': [1, 3, 5, 7, 10, 20]}
params_svr = {'kernel':['linear','rbf'], 'C':[1, 10, 100, 1000, 5000, 10000]}
params_rfc = {'n_estimators':[100, 250, 500, 750, 1000, 2000]}

# k-fold cross validation
cross_validation = 5

# execute kNN
knn, results_knn, mse_knn = kNNRegression(training_data, training_labels, testing_data, testing_labels, params=params_knn, cv=cross_validation)
# execute SVR
svr, results_svr, mse_svr = SVRegression(training_data, training_labels, testing_data, testing_labels, params=params_svr, cv=cross_validation)

# number of iterations (RF Regression)
iterations = 3
results_rfc = mse_rfc = 0

# find the best parameter for the RFC first
n_estimators = ParamsRandomTreeRegression(training_data, training_labels, params=params_rfc, cv=cross_validation)

for x in range(0,iterations):
    rfc, results, mse = RandomTreeRegression(training_data, training_labels, testing_data, testing_labels, n_estimators=n_estimators)
    results_rfc += results
    mse_rfc += mse
    
results_rfc /= iterations
mse_rfc /= iterations

# size of the random sample for the signifigance test
nbrOfParticipants = 400

rnd_indices_1 = sample(xrange(len(results_knn)), nbrOfParticipants)
rnd_indices_2 = sample(xrange(len(results_knn)), nbrOfParticipants)
rnd_indices_3 = sample(xrange(len(results_knn)), nbrOfParticipants)

# execute the Wilcoxon-Signed-Rank test
p_val_knn_svr = stats.wilcoxon(results_knn[rnd_indices_1], results_svr[rnd_indices_1])[1]
p_val_rfc_svr = stats.wilcoxon(results_rfc[rnd_indices_2], results_svr[rnd_indices_2])[1]
p_val_knn_rfc = stats.wilcoxon(results_knn[rnd_indices_3], results_rfc[rnd_indices_3])[1]

true_pred_knn = np.reshape(np.append(results_knn, np.append(testing_labels, (np.ones([testing_labels.size, 1]) * pow(mse_knn, 0.5)))), [testing_labels.size, 3], 'F')
true_pred_svr = np.reshape(np.append(results_svr, np.append(testing_labels, (np.ones([testing_labels.size, 1]) * pow(mse_svr, 0.5)))), [testing_labels.size, 3], 'F')
true_pred_rfc = np.reshape(np.append(results_rfc, np.append(testing_labels, (np.ones([testing_labels.size, 1]) * pow(mse_rfc, 0.5)))), [testing_labels.size, 3], 'F')

np.savetxt("results/regression/true_pred_knn.dat", true_pred_knn, delimiter="\t")
np.savetxt("results/regression/true_pred_svr.dat", true_pred_svr, delimiter="\t")
np.savetxt("results/regression/true_pred_rfc.dat", true_pred_rfc, delimiter="\t")