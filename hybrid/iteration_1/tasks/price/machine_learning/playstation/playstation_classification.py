# -*- coding: utf-8 -*-
import numpy as np
import csv, math

from sklearn import neighbors, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error
from sklearn.preprocessing import normalize
from scipy import stats

def SVClassification(training_data, training_labels, testing_data, testing_labels, params={'C':[1, 5, 10]}, cv=5):
		# initialise k-fold cross-validation grid search
    clf = GridSearchCV(svm.LinearSVC(), params, cv=cv)
    clf.fit(training_data, training_labels)
		# train the linear support vector machine
    svc = svm.LinearSVC(C=clf.best_estimator_.C).fit(training_data, training_labels)
		# predict the results of the test data
    results = svc.predict(testing_data)
		# evaluate the results
    acc = accuracy_score(testing_labels, results)
    mae = mean_absolute_error(testing_labels, results)
    conf_mat = confusion_matrix(testing_labels, results, range(1,int(max(testing_labels))))
    return svc, results, acc, mae, conf_mat

def kNNClassification(training_data, training_labels, testing_data, testing_labels, params={'n_neighbors':[1, 5, 10]}, cv=5):
		# initialise k-fold cross-validation grid search
    clf = GridSearchCV(neighbors.KNeighborsClassifier(), params, cv=cv)
    clf.fit(training_data, training_labels)
		# train the kNN		
    knn = neighbors.KNeighborsClassifier(n_neighbors=clf.best_estimator_.n_neighbors).fit(training_data, training_labels)
		# predict the results of the test data		
    results = knn.predict(testing_data)
		# evaluate the results		
    acc = accuracy_score(testing_labels, results)
    mae = mean_absolute_error(testing_labels, results)
    conf_mat = confusion_matrix(testing_labels, results, range(1,int(max(testing_labels))))
    return knn, results, acc, mae, conf_mat
    
def RandomTreeClassification(training_data, training_labels, testing_data, testing_labels, n_estimators=10):
		# train the random forest tree
    rfc = RandomForestClassifier(n_estimators=n_estimators).fit(training_data, training_labels)
		# predict the results of the test data		
    results = rfc.predict(testing_data)
		# evaluate the results		
    acc = accuracy_score(testing_labels, results)
    mae = mean_absolute_error(testing_labels, results)
    conf_mat = confusion_matrix(testing_labels, results, range(1,int(max(testing_labels))))
    return rfc, results, acc, mae, conf_mat
    
def ParamsRandomTreeClassification(training_data, training_labels, params={'n_estimators':[1, 5, 10]}, cv=5):
		# initialise k-fold cross-validation grid search
    clf = GridSearchCV(RandomForestClassifier(), params, cv=cv)
    clf.fit(training_data, training_labels)
    return clf.best_estimator_.n_estimators

def gtest(f_obs, f_exp=None, ddof=0):
		# calculate the g-value based on the formula from http://en.wikipedia.org/wiki/G-test
    value = f_obs * np.log(f_obs / f_exp)
    value[np.where(np.isnan(value) == True)] = 0
    g = 2 * np.sum(value)
    return g, stats.chisqprob(g, ddof)
    
def significanceTest(conf_A, conf_B):
		# build up the contingency tables
    freq_A = np.sum(conf_A, axis=0)
    freq_B = np.sum(conf_B, axis=0)
    
    if size(np.where(freq_A != 0)) > size(np.where(freq_B != 0)):
        indices_A_B = np.where(freq_A != 0)
    else:
        indices_A_B = np.where(freq_B != 0)
    # calculate the expectation values
    freq_A_B = np.reshape(np.append(freq_A[indices_A_B], freq_B[indices_A_B], axis=0), [2, size(indices_A_B)])
    sum_A_B = sum(freq_A_B)
    proportions_classes_A_B = np.reshape(np.divide(sum(freq_A_B, axis=0), np.asfarray(sum_A_B)), [1, size(indices_A_B)])
    sum_A_B = np.reshape(np.sum(freq_A_B, axis=1), [1, 2])
    exp_values_A_B = np.multiply(sum_A_B.transpose(), proportions_classes_A_B)
    obs_A_B = np.reshape(np.append(np.sum(conf_A, axis=0)[indices_A_B], np.sum(conf_B, axis=0)[indices_A_B], axis=0), [2, size(indices_A_B)])
		# calculate the g and p value
    g_A_B, p_A_B = gtest(obs_A_B, exp_values_A_B, (size(obs_A_B, 0) - 1) * (size(obs_A_B, 1) - 1))
    
    return p_A_B
    
fname = '../../../../../training_data/playstation/train/trainDataLabeledNormalized.csv'

reader = csv.reader(open(fname,"rb"),delimiter='\t')
next(reader)
x = list(reader)
data = np.array(x).astype('float')

training_labels = data[:,-1]
training_data = data[:,0:-1]

fname = '../../../../../training_data/playstation/test/testDataLabeledNormalized.csv'

reader = csv.reader(open(fname,"rb"),delimiter='\t')
next(reader)
x = list(reader)
data = np.array(x).astype('float')

testing_labels = data[:,-1]
testing_data = data[:,0:-1]

# grid search parameters of the machine learning algorithms
params_svc = {'C':[1, 10, 100, 1000, 5000, 10000]}
params_knn = {'n_neighbors':[1, 3, 5, 7, 10, 20], 'weights':['uniform','distance']}
params_rfc = {'n_estimators':[100, 250, 500, 750, 1000, 2000]}

# k-fold cross validation
cross_validation = 5

# execute linear SVC
svc, results_svc, acc_svc, mae_svc, conf_svc = SVClassification(training_data, training_labels, testing_data, testing_labels, params=params_svc, cv=cross_validation)
# execute kNN
knn, results_knn, acc_knn, mae_knn, conf_knn = kNNClassification(training_data, training_labels, testing_data, testing_labels, params=params_knn, cv=cross_validation)

# number of iterations (RFC)
iterations = 3
results_rfc = acc_rfc = mae_rfc = conf_rfc = 0

# find the best parameter for the RFC first
n_estimators = ParamsRandomTreeClassification(training_data, training_labels, params=params_rfc, cv=cross_validation)

for x in range(0,iterations):
		# execute the random forest classifier
    rfc, results, acc, mae, conf = RandomTreeClassification(training_data, training_labels, testing_data, testing_labels, n_estimators=n_estimators)
    results_rfc += results
    acc_rfc += acc
    mae_rfc += mae
    conf_rfc += conf

# average the results    
results_rfc /= iterations
for x in range(0,len(results_rfc)):
    results_rfc[x] = math.floor(results_rfc[x])
    
acc_rfc /= iterations
mae_rfc /= iterations
conf_rfc /= iterations
for x in range(0,size(conf_rfc, 0)):
    for y in range(0,size(conf_rfc, 1)):
        conf_rfc[x][y] = math.floor(conf_rfc[x][y])
        
p_svc_knn = significanceTest(conf_svc, conf_knn)
p_svc_rfc = significanceTest(conf_svc, conf_rfc)
p_rfc_knn = significanceTest(conf_rfc, conf_knn)

# normalise the confusion matrices
conf_svc = normalize(conf_svc.astype(float), norm='l1')
conf_knn = normalize(conf_knn.astype(float), norm='l1')
conf_rfc = normalize(conf_rfc.astype(float), norm='l1')

np.savetxt("results/classification/conf_mat_rfc.dat", conf_rfc, delimiter="\t")
np.savetxt("results/classification/conf_mat_knn.dat", conf_knn, delimiter="\t")
np.savetxt("results/classification/conf_mat_svc.dat", conf_svc, delimiter="\t")

np.savetxt("results/classification/knn.txt", (acc_knn, mae_knn))
np.savetxt("results/classification/svc.txt", (acc_svc, mae_svc))
np.savetxt("results/classification/rfc.txt", (acc_rfc, mae_rfc))
