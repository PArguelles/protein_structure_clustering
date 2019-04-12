

import ClusteringEvaluation as ce
import MatrixFunctions as mf
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering

import numpy as np

matrix1 = np.load('C:/Users/pedro.arguelles/Desktop/scripts/matrix_a.3._maxsub')
matrix2 = np.load('C:/Users/pedro.arguelles/Desktop/scripts/matrix_a.3._rmsd')

matrix1 = mf.minMaxScale(matrix1)
matrix2 = mf.minMaxScale(matrix2)

corr = matrix1 + matrix2

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=5, linkage="complete").fit(corr)
metrics = ce.clusterEvaluationNoLabels(corr, agglomerative.labels_)
print(metrics)

matrix1 = mf.calculateDistances(matrix1)
corr = matrix1 + matrix2

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=5, linkage="complete").fit(corr)
metrics = ce.clusterEvaluationNoLabels(corr, agglomerative.labels_)
print(metrics)

matrix2 = mf.calculateDistances(matrix2)
corr = matrix1 + matrix2

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=5, linkage="complete").fit(corr)
metrics = ce.clusterEvaluationNoLabels(corr, agglomerative.labels_)
print(metrics)

print("")