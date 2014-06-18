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
    clf = GridSearchCV(neighbors.KNeighborsRegressor(), params, cv=cv)
    clf.fit(training_data, training_labels)
    knn = neighbors.KNeighborsRegressor(n_neighbors=clf.best_estimator_.n_neighbors).fit(training_data, training_labels)
    results = knn.predict(testing_data)
    mse = mean_squared_error(testing_labels, results)
    return knn, results, mse
    
def LassoRegression(training_data, training_labels, testing_data, testing_labels, params={'alpha':[0.1, 0.5]}, cv=5):
    clf = GridSearchCV(linear_model.Lasso(), params, cv=cv)
    clf.fit(training_data, training_labels)
    lasso = linear_model.Lasso(alpha=clf.best_estimator_.alpha, max_iter=clf.best_estimator_.max_iter).fit(training_data, training_labels)
    results = lasso.predict(testing_data)
    mse = mean_squared_error(testing_labels, results)    
    return lasso, results, mse
    
def SVRegression(training_data, training_labels, testing_data, testing_labels, params={'C':[1, 5, 10]}, cv=5):
    clf = GridSearchCV(svm.SVR(), params, cv=cv)
    clf.fit(training_data, training_labels)
    svr = svm.SVR(kernel=clf.best_estimator_.kernel, C=clf.best_estimator_.C).fit(training_data, training_labels)
    results = svr.predict(testing_data)
    mse = mean_squared_error(testing_labels, results)
    return svr, results, mse
    
def RandomTreeRegression(training_data, training_labels, testing_data, testing_labels, n_estimators=10):
    rfc = RandomForestRegressor(n_estimators=n_estimators).fit(training_data, training_labels)
    results = rfc.predict(testing_data)
    mse = mean_squared_error(testing_labels, results)
    return rfc, results, mse
    
def ParamsRandomTreeRegression(training_data, training_labels, params={'n_estimators':[1, 5, 10]}, cv=5):
    clf = GridSearchCV(RandomForestRegressor(), params, cv=cv)
    clf.fit(training_data, training_labels)
    return clf.best_estimator_.n_estimators
    
fname = '../../../../../training_data/iphone/train/trainingDataNormalized.csv'

reader = csv.reader(open(fname,"rb"),delimiter='\t')
next(reader)
x = list(reader)
data = np.array(x).astype('float')

training_labels = data[:,-1]
training_data = data[:,0:-1]

testing_data = [0.2, 3/7, 1/3, 0.966, 0.0833333333333, 0.222222222222, 0.666666666667, 288/500000, 0.666666666667, 0.166666666667, 0.95652173913, 0.1, 1.0, 1.0, 1.0, 0.0]
testing_labels = [185]

params_rfc = {'n_estimators':[100, 250, 500, 750, 1000, 2000]}

cross_validation = 5

iterations = 3
results_rfc = mse_rfc = 0

n_estimators = ParamsRandomTreeRegression(training_data, training_labels, params=params_rfc, cv=cross_validation)

for x in range(0,iterations):
    rfc, results, mse = RandomTreeRegression(training_data, training_labels, testing_data, testing_labels, n_estimators=n_estimators)
    results_rfc += results
    mse_rfc += mse
    
results_rfc /= iterations
mse_rfc /= iterations

