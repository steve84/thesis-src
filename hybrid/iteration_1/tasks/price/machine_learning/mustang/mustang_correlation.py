# -*- coding: utf-8 -*-
import numpy as np
import csv

from scipy import stats

def calc_correlation(fname):    
    reader = csv.reader(open(fname,"rb"),delimiter='\t')
    next(reader)
    x = list(reader)
    data = np.array(x).astype('float')
    
    normal_a = stats.normaltest(data[:,0])[1]
    normal_b = stats.normaltest(data[:,1])[1]
    
    if (normal_a >= 0.05) & (normal_b >= 0.05):
		# both series are normally distributed
        return stats.pearsonr(data[:,0], data[:,1])[0]
    else:
		# not normally distributed
        return stats.spearmanr(data[:,0], data[:,1])[0]
        
corr_knn = calc_correlation('results/regression/true_pred_knn.dat')
corr_svr = calc_correlation('results/regression/true_pred_svr.dat')
corr_rfc = calc_correlation('results/regression/true_pred_rfc.dat')