
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering



# load protein data before loop
path_to_results = 'C:/ShareSSD/scop/clustering_results_single/'
measure1 = 'maxsub'
measure2 = 'maxsub'
measure3 = 'maxsub'

sample_for_domains = 'b.2'
sample = 'b.2.'

path_to_matrix = 'C:/ShareSSD/scop/tests/matrix_'+sample+'_'+measure1

matrix1 = np.load(path_to_matrix)
matrix2 = matrix1
matrix3 = matrix1

domains = rs.loadDomainListFromFile(sample)

n_labels = scop.getUniqueClassifications(sample_for_domains)
ground_truth = scop.getDomainLabels(domains)
ground_truth = map(int, ground_truth)
ground_truth = list(map(int, ground_truth))

matrix1 = mf.minMaxScale(matrix1)
matrix2 = mf.minMaxScale(matrix2)
matrix3 = mf.minMaxScale(matrix3)

matrix1 = mf.calculateDistances(matrix1)
matrix2 = mf.calculateDistances(matrix2)
matrix3 = mf.calculateDistances(matrix3)

w1 = 1
w2 = 0
w3 = 0

corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)

# Hierarchical
for link in ['complete','average']:
    agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(corr)
    labels = agglomerative.labels_
    metrics = ce.clusterEvaluation(corr, labels, ground_truth)
    print(metrics)
    #ce.saveResultsWithWeights(measure1, measure2, w1, 'hierarchical_'+link, sample, metrics)

# K-Medoids
medoids, clusters = km.kMedoids(corr, n_labels, 100)
labels = km.sortLabels(clusters)
metrics = ce.clusterEvaluation(corr, labels, ground_truth)
#ce.saveResultsWithWeights(measure1, measure2, w1, 'kmedoids', sample, metrics)
