
from sklearn import metrics

def clusterEvaluation(X, labels, labels_true):
    values = []
    values.append(metrics.homogeneity_score(labels_true, labels))
    values.append(metrics.completeness_score(labels_true, labels))
    values.append(metrics.v_measure_score(labels_true, labels))
    values.append(metrics.adjusted_rand_score(labels_true, labels))
    values.append(metrics.adjusted_mutual_info_score(labels_true, labels))
    values.append(metrics.calinski_harabaz_score(X, labels))
    values.append(metrics.silhouette_score(X, labels, metric='precomputed'))
    return values

def clusterEvaluationNoLabels(X, labels):
    values = []
    values.append(metrics.calinski_harabaz_score(X, labels))
    values.append(metrics.silhouette_score(X, labels, metric='precomputed'))
    return values

def saveResults(measure1, measure2, algorithm, sample, metrics):

    path_to_results = 'C:/ShareSSD/scop/clustering_results_single_matrix/'
    
    with open(path_to_results+algorithm+'_'+sample+'_'+measure1+'_'+measure2, 'w') as nf:
        nf.write('# Cluster evaluation: \n')
        #nf.write('Individual: '+'-'.join(str(individual)))
        nf.write('Homogeneity: %0.3f \n' % metrics[0])
        nf.write('Completeness: %0.3f \n' % metrics[1])
        nf.write('V-measure: %0.3f \n' % metrics[2])
        #nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
        nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
        nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
        nf.write('Silhouette coefficient: %0.3f \n' % metrics[6]) 

def saveResultsWithSequenceWeights(measure1, measure2, w1, algorithm, sample, metrics):

    path_to_results = 'C:/ShareSSD/scop/clustering_results_seq/'
    
    with open(path_to_results+algorithm+'_'+sample+'_'+measure1+'_'+measure2+'_'+str(w1), 'w') as nf:
        nf.write('# Cluster evaluation: \n')
        nf.write('Measures: '+measure1+' '+measure2+'\n')
        nf.write('Weights: '+str(w1)+' '+str(1-w1)+'\n')
        nf.write('Homogeneity: %0.3f \n' % metrics[0])
        nf.write('Completeness: %0.3f \n' % metrics[1])
        nf.write('V-measure: %0.3f \n' % metrics[2])
        #nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
        nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
        nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
        nf.write('Silhouette coefficient: %0.3f \n' % metrics[6])

def saveResultsWithWeights(measure1, measure2, w1, algorithm, sample, metrics):

    path_to_results = 'C:/ShareSSD/scop/clustering_results_pair/'
    
    with open(path_to_results+algorithm+'_'+sample+'_'+measure1+'_'+measure2+'_'+str(w1), 'w') as nf:
        nf.write('# Cluster evaluation: \n')
        nf.write('Measures: '+measure1+' '+measure2+'\n')
        nf.write('Weights: '+str(w1)+' '+str(1-w1)+'\n')
        nf.write('Homogeneity: %0.3f \n' % metrics[0])
        nf.write('Completeness: %0.3f \n' % metrics[1])
        nf.write('V-measure: %0.3f \n' % metrics[2])
        #nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
        nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
        nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
        nf.write('Silhouette coefficient: %0.3f \n' % metrics[6]) 

def saveResultsCombined(measure1, measure2, w1, w2, w3, algorithm, sample, metrics):

    path_to_results = 'C:/ShareSSD/scop/clustering_results_combined/'
    
    with open(path_to_results+algorithm+'_'+sample+'_'+measure1+'_'+measure2+'_'+str(w1)+'_'+str(w2)+'_'+str(w3), 'w') as nf:
        nf.write('# Cluster evaluation: \n')
        nf.write('Measures: '+measure1+' '+measure2+'\n')
        nf.write('Weights: '+str(w1)+' '+str(w2)+' '+str(w3)+'\n')
        nf.write('Homogeneity: %0.3f \n' % metrics[0])
        nf.write('Completeness: %0.3f \n' % metrics[1])
        nf.write('V-measure: %0.3f \n' % metrics[2])
        #nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
        nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
        nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
        nf.write('Silhouette coefficient: %0.3f \n' % metrics[6])