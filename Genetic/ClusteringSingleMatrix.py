
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering

algorithms = ['complete','average','kmedoids']
measures = ['rmsd','gdt_2','gdt_4','tm','maxsub','seq']
samples = ['a.1','a.3','b.2','b.3']

for m in measures:
    for alg in algorithms:
        for spl in samples:

            # load protein data before loop
            path_to_results = 'C:/ShareSSD/scop/clustering_results_single_matrix/'
            measure1 = m

            sample_for_domains = spl
            sample = str(spl)+'.'
            
            matrix1 = rs.loadMatrixFromFile(sample, measure1)
            matrix1 = mf.minMaxScale(matrix1)
            matrix1 = mf.calculateDistances(matrix1)

            domains = rs.loadDomainListFromFile(sample)

            n_labels = scop.getUniqueClassifications(sample_for_domains)

            ground_truth = scop.getDomainLabels(domains)
            ground_truth = map(int, ground_truth)
            ground_truth = list(map(int, ground_truth))

            w1 = 1

            # Hierarchical
            for link in ['complete','average']:
                agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage=link).fit(matrix1)
                labels = agglomerative.labels_
                metrics = ce.clusterEvaluation(matrix1, labels, ground_truth)
                ce.saveResults(measure1, measure1, link, sample, metrics)
                print(metrics)

            # K-Medoids
            medoids, clusters = km.kMedoids(matrix1, n_labels, 100)
            labels = km.sortLabels(clusters)
            metrics = ce.clusterEvaluation(matrix1, labels, ground_truth)
            ce.saveResults(measure1, measure1, 'kmedoids', sample, metrics)
            print(metrics)
