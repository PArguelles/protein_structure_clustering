

from sklearn.cluster import AffinityPropagation
from sklearn import metrics

import MatrixFunctions as mf
import ClusteringEvaluation as ce

import numpy as np

matrix = np.load('C:/Users/pedro.arguelles/Desktop/scripts/matrix_a.3._rmsd')

matrix = mf.minMaxScale(matrix)
matrix = mf.calculateDistances(matrix)

max = [0,0]

for preference in np.arange(-1000, 20, 50):
    for damping in np.arange(0.5,1.0,0.1):

        af = AffinityPropagation(preference=preference).fit(matrix)
        labels = af.labels_
        metrics = ce.clusterEvaluationNoLabels(matrix, labels)
        if metrics[1] > max[1]:
            max = metrics

        print(metrics)

print(max)
print()