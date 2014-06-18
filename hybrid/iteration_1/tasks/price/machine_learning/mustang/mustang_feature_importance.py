# -*- coding: utf-8 -*-

import numpy as np
import csv

from sklearn.svm import SVR
from sklearn.feature_selection import RFECV

fname = '../../../../../training_data/mustang/train/trainingDataNormalized.csv'

reader = csv.reader(open(fname,"rb"),delimiter='\t')
next(reader)
x = list(reader)
data = np.array(x).astype('float')

labels = data[:,-1]
training_data = data[:,0:-1]

# create a linear support vector machine with C=100 (Recommended by http://link.springer.com/article/10.1023%2FA%3A1012487302797)
svc = SVR(kernel='linear', C=100)
# initialise recursive feature elimination
rfe = RFECV(estimator=svc, step=1, cv=5)
rfe.fit(training_data, labels)

reader = csv.reader(open(fname,"rb"),delimiter='\t')
header = reader.next()
header = header[:-1]

indices = np.where(rfe.support_ == True)[0]

print('Reduced features from ' + str(len(rfe.support_)) + ' to ' + str(len(indices)) + ':')
for x in indices:
    print(header[x])

indices = np.where(rfe.support_ == False)[0]
    
print('\nUseless features:')
for x in indices:
    print(header[x])