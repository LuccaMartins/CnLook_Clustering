from dtaidistance import dtw_ndim
from sklearn import metrics
import numpy as np
from scipy.spatial import distance_matrix as euclidian_distance_matrix
from scipy.cluster.hierarchy import linkage, dendrogram

from Clustering_Framework.ClusteringMethods.FOSC.util.fosc import FOSC
from Clustering_Framework.ClusteringMethods.FOSC.util.plotting import plotDendrogram, plotPartition

#TODO: test with FOSC and K-means (with Elbow method)

def startFOSC(X, savePath=None):
    # Calculating distance matrix
    mat = generateDistanceMatrix(X, 'euclidian')

    listOfMClSize = [2, 4, 5, 8, 16, 20, 30]
    methodsLinkage = ["single", "average", "ward", "complete", "weighted"]
    results = []

    for m in listOfMClSize:
        print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)

        for lm in methodsLinkage:
            print("Calling linkage with " + lm + " passing the distances matrix...")
            Z = linkage(mat, method=lm)

            foscFramework = FOSC(Z, mClSize=m)
            infiniteStability = foscFramework.propagateTree()
            partition = foscFramework.findProminentClusters(1, infiniteStability)

            # validação do algoritmo: silhouette ou AUC Under Curve
            if len(set(partition)) > 1:
                silhouette = metrics.silhouette_score(mat, partition, metric="precomputed")
                results.append({'MinClusterSize': m,
                                'Linkage Method': lm,
                                'Partition': partition,
                                'Silhouette': silhouette
                })
            else:
                results.append({'MinClusterSize': m,
                                'Linkage Method': lm,
                                'Partition': partition,
                                'Silhouette': -1
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