
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering

# load protein data before loop

measure1 = 'rmsd'
measure2 = 'seq'
measure3 = 'seq'

sample = 'a.1.'
sample_for_domains = 'a.1'

matrix1 = rs.loadMatrixFromFile(sample, measure1)
matrix2 = rs.loadMatrixFromFile(sample, measure2)
matrix3 = rs.loadMatrixFromFile(sample, measure3)

#matrix3 = 1 - matrix3

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

for w1 in np.arange(0.00,1.05,0.05):
    print(w1)
    w2 = 0
    w3 = 1-w1

    corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)

    # Hierarchical
    for link in ['complete']:
        agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(corr)
        labels = agglomerative.labels_
        metrics = ce.clusterEvaluation(corr, labels, ground_truth)
        print(metrics)