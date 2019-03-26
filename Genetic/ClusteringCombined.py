
import ClusteringEvaluation as ce
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering


combinations = [('rmsd','gdt_2'),('rmsd','gdt_4'),
                ('rmsd','maxsub'),('rmsd','tm'),
                ('gdt_2','gdt_4'),('gdt_2','maxsub'),
                ('gdt_2','tm'), ('gdt_4','maxsub'),
                ('gdt_4','tm'), ('maxsub','tm')]

for m1, m2 in combinations:
    for spl in ['a.1','a.3','b.2','b.3']:

        # load protein data before loop
        path_to_results = 'C:/ShareSSD/scop/clustering_results_combined/'
        measure1 = m1
        measure2 = m2
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

        for w1 in np.arange(0.00,1.01,0.01):
            #for w2 in np.arange(0.05,1.00,0.05):
            w2 = 1-w1
            w3 = 0
                    
            corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)

            # Hierarchical
            for link in ['complete','average']:
                agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage=link).fit(corr)
                labels = agglomerative.labels_
                metrics = ce.clusterEvaluation(corr, labels, ground_truth)
                ce.saveResultsCombined(measure1, measure2, w1, w2, w3, link, sample, metrics)
                print(metrics)

            try:
                # K-Medoids
                medoids, clusters = km.kMedoids(corr, n_labels, 100)
                labels = km.sortLabels(clusters)
                metrics = ce.clusterEvaluation(corr, labels, ground_truth)
                ce.saveResultsCombined(measure1, measure2, w1, w2, w3, 'kmedoids', sample, metrics)
                print(metrics)
            except:
                pass
