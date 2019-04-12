import ClusteringEvaluation as ce
import MatrixFunctions as mf


from sklearn.neighbors import NearestNeighbors
import numpy as np

matrix = np.load('C:/Users/pedro.arguelles/Desktop/scripts/matrix_a.3._rmsd')


nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(matrix)
distances, indices = nbrs.kneighbors(matrix)



print(indices)
print()