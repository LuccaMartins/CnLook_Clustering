from dtaidistance import dtw_ndim
from sklearn import metrics
from validclust import dunn
from scipy.spatial import distance_matrix as euclidian_distance_matrix
from scipy.spatial.distance import squareform

from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import KMeans, DBSCAN

from Clustering_Framework.ClusteringMethods.FOSC.util.fosc import FOSC
from Clustering_Framework.ClusteringMethods.FOSC.util.plotting import plotDendrogram, plotPartition
from Clustering_Framework.ClusterValidation.cluster_validation import *

#TODO: test with FOSC and K-means (with Elbow method)

def adjustPartition(partition, method):
    #noise = 0
    for i, label in enumerate(partition):
        if label == -1:
            partition[i] = 0
        else:
            partition[i] = label + 1
    # if method == 'FOSC':
    #     for i, label in enumerate(partition):
    #         if label == -1:
    #             partition[i] = 0
    #         else:
    #             partition[i] = label + 1
    # # elif method == 'K-Means':
    # elif method == 'DBSCAN':
    #     for i, label in enumerate(partition):
    #         if label == -1:
    #             partition[i] = 0
    #         else:
    #             partition[i] = label + 1
    return partition

def startDBSCAN(X):
    print('Running DBSCAN...')
    # Calculating distance matrix
    mat = generateDistanceMatrix(X, 'euclidian')
    eps_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    results = []
    min_list = [5, 10, 15, 20, 25]
    for min_samples in min_list:
        for eps in eps_list:
            db = DBSCAN(eps, min_samples=min_samples, metric='precomputed').fit(mat)
            # print('Getting Cluster Validation...')
            cv = getClusterValidation(X, mat, adjustPartition(db.labels_, 'DBSCAN'))
            results.append({'Method': 'DBSCAN',
                            'Method Info': {
                                'Eps': eps,
                                'Min Samples': min_samples
                            },
                            'Data': X,
                            'Partition': adjustPartition(db.labels_, 'DBSCAN'),
                            'Distance Matrix': mat,
                            'Cluster Validation': cv
                            })

    return results

def startKMeans(X):
    print('Running K-Means...')
    # Calculating distance matrix
    mat = generateDistanceMatrix(X, 'euclidian')
    k_clusters = [3, 4, 5]
    results = []

    for k in k_clusters:
        kmeans = KMeans(k)
        kmeans.fit(X)
        partition = kmeans.predict(X)
        results.append({'Method': 'K-Means',
                        'Method Info': {
                            'K': k,
                        },
                        'Data': X,
                        'Partition': adjustPartition(partition, 'K-Means'),
                        'Distance Matrix': mat,
                        'Cluster Validation': getClusterValidation(X, mat, adjustPartition(partition, 'K-Means'))
                        })

    return results

def startFOSC(X, savePath=None):
    print('Running FOSC...')
    # Calculating distance matrix
    mat = generateDistanceMatrix(X, 'euclidian')

    listOfMClSize = [4, 5, 8, 16, 20, 30]
    methodsLinkage = ["single", "average", "ward", "complete", "weighted"]
    results = []

    for m in listOfMClSize:
        # print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)
        for lm in methodsLinkage:
            # print("Calling linkage with " + lm + " passing the distances matrix...")
            condensed_mat = squareform(mat)
            Z = linkage(condensed_mat, method=lm)

            foscFramework = FOSC(Z, mClSize=m)
            infiniteStability = foscFramework.propagateTree()
            partition = foscFramework.findProminentClusters(1, infiniteStability)

            results.append({'Method': 'FOSC',
                            'Method Info': {
                                'MinClusterSize': m,
                                'Linkage Method': lm,
                                'Hierarchy': Z
                            },
                            'Data': X,
                            'Partition': adjustPartition(partition, 'FOSC'),
                            # 'Distance Matrix': mat,
                            'Cluster Validation': getClusterValidation(X, mat, adjustPartition(partition, 'FOSC'))
                            })

            if savePath != None:
                titlePlot = f"{savePath}, mClSize: {m}\nLinkage Method: {lm}, Num of Objects: {len(X)}"
                saveDendrogram = f"./FOSC Results/Dendrogram {savePath} - mClSize {m} - {lm}.png"

                # Plot results
                plotDendrogram(Z, partition, titlePlot, saveDendrogram)
                #plotDendrogram(Z, partition, titlePlot)

    return results

def generateDistanceMatrix(X, metric):
    # drop 'tracking_status'
#     X = [np.array([s[1:] for s in record], dtype=np.double) for record in X]

    if metric == 'dtw':
        # get a sample to count the features (dimensions) - not working right now
        n_dimensions = len(X[0][0])
        # print(f"Producing distance matrix with DTW for {len(X)} series of {n_dimensions}-dimensions...")
        mat = dtw_ndim.distance_matrix_fast(X, n_dimensions)
    elif metric == 'euclidian':
        # print(f"Producing distance matrix with Euclidian Distance for {len(X)} series of {1}-dimensions...")
        mat = euclidian_distance_matrix(X, X)

    return mat