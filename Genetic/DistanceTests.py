

import ClusteringEvaluation as ce
import MatrixFunctions as mf
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering

import numpy as np

# distance calculation is necessary for maxsub

matrix = np.load('C:/Users/pedro.arguelles/Desktop/scripts/matrix_a.3._gdt_2')

matrix = mf.calculateDistances(matrix)

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=5, linkage="complete").fit(matrix)
metrics = ce.clusterEvaluationNoLabels(matrix, agglomerative.labels_)
print(metrics)

print("")


