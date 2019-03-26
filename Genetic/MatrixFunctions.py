
import numpy as np
import sklearn.preprocessing as pp
from sklearn.metrics.pairwise import euclidean_distances

def symmetrizeMatrix(a):
        return a + a.T - np.diag(a.diagonal())

def calculateDistances(a):
        corr = euclidean_distances(a,a)
        return corr

def minMaxScale(matrix):
        maxv = np.amax(matrix)
        minv = np.amin(matrix)
        matrix = ((matrix - minv)/(maxv - minv))
        return matrix

def calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3):

        matrix1 = np.asmatrix(matrix1)
        matrix2 = np.asmatrix(matrix2)
        matrix3 = np.asmatrix(matrix3)

        matrix1 *= w1
        matrix2 *= w2
        matrix3 *= w3

        corr = matrix1 + matrix2 + matrix3

        return corr