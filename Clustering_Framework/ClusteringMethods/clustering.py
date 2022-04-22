from Clustering_Framework.ClusteringMethods.clustering_methods import *
from Clustering_Framework.clustering_parameters import *


def startClusteringTests(X):
    FOSC_results = startFOSC(X)
    results = []
    for method in clustering_methods:
        if method == 'FOSC':
            results.append({'Method': method, 'Results': startFOSC(X)})
        elif method == 'K-Means':
            print('K-Means to be implemented...')
    return results