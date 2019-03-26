
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering


for measure in ['rmsd','gdt_2','gdt_4','tm','maxsub']:
    for spl in ['a.1','a.3','b.2','b.3']:

        # load protein data before loop
        path_to_results = 'C:/ShareSSD/scop/clustering_results_seq/'
        measure1 = measure
        measure2 = measure
        measure3 = 'seq'

        sample_for_domains = spl
        sample = str(spl)+'.'
        
        matrix1 = rs.loadMatrixFromFile(sample, measure1)
        matrix2 = rs.loadMatrixFromFile(sample, measure2)
        matrix3 = rs.loadMatrixFromFile(sample, measure3)

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

        for w1 in np.arange(0.05,1.05,0.05):

            w2 = 0
            w3 = 1-w1
            
            corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)

            # Hierarchical
            for link in ['complete','average']:
                agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage=link).fit(corr)
                labels = agglomerative.labels_
                metrics = ce.clusterEvaluation(corr, labels, ground_truth)
                ce.saveResultsWithSequenceWeights(measure1, measure3, w1, link, sample, metrics)
                print(metrics)

            # K-Medoids
            medoids, clusters = km.kMedoids(corr, n_labels, 100)
            labels = km.sortLabels(clusters)
            metrics = ce.clusterEvaluation(corr, labels, ground_truth)
            ce.saveResultsWithSequenceWeights(measure1, measure3, w1, 'kmedoids', sample, metrics)
            print(metrics)
