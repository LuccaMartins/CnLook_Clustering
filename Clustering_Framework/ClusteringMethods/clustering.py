from Clustering_Framework.ClusteringMethods.clustering_methods import *
from Clustering_Framework.clustering_parameters import *


def startClusteringTests(X):
    results = []
    for method in clustering_methods:
        if method == 'FOSC':
            for result in startFOSC(X):
                results.append(result)
        elif method == 'K-Means':
            for result in startKMeans(X):
                results.append(result)
        elif method == 'DBSCAN':
            for result in startDBSCAN(X):
                results.append(result)
    return results