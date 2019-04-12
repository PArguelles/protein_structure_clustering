

import ClusteringEvaluation as ce
import MatrixFunctions as mf
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering

import numpy as np

matrix = np.load('C:/Users/pedro.arguelles/Desktop/scripts/matrix_a.3._maxsub')

#matrix = mf.minMaxScale(matrix)
matrix = mf.calculateDistances(matrix)

sc = SpectralClustering(n_clusters=5, affinity='nearest_neighbors', assign_labels="kmeans", random_state=100, n_jobs=-1).fit(matrix)
metrics = ce.clusterEvaluationNoLabels(matrix, sc.labels_)
print(metrics)

sc = SpectralClustering(n_clusters=5, affinity='nearest_neighbors', n_neighbors=20, assign_labels="kmeans", random_state=100, n_jobs=-1).fit(matrix)
metrics = ce.clusterEvaluationNoLabels(matrix, sc.labels_)
print(metrics)

sc = SpectralClustering(n_clusters=5, affinity='nearest_neighbors', n_neighbors=50, assign_labels="kmeans", random_state=100, n_jobs=-1).fit(matrix)
metrics = ce.clusterEvaluationNoLabels(matrix, sc.labels_)
print(metrics)

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=5, linkage="complete").fit(matrix)
metrics = ce.clusterEvaluationNoLabels(matrix, agglomerative.labels_)
print(metrics)

print("")


