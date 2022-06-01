from Clustering_Framework.ClusteringMethods.clustering_methods import *
from Clustering_Framework.clustering_parameters import *


def startClusteringTests(X):
    results = []
    mat = generateDistanceMatrix(X, 'euclidian')
    for method in clustering_methods:
        if method == 'FOSC':
            for result in startFOSC(X, mat):
                results.append(result)
        elif method == 'K-Means':
            for result in startKMeans(X, mat):
                results.append(result)
        elif method == 'DBSCAN':
            for result in startDBSCAN(X, mat):
                results.append(result)
    return results