from dtaidistance import dtw_ndim
from sklearn import metrics

def startFOSC(X, savePath=None):
    # Calculating distance matrix
    mat = generateDistanceMatrix(X, 'dtw')

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
                results.append([m, lm, partition, silhouette])
            else:
                results.append([m, lm, partition, -1])

            if savePath != None:
                titlePlot = f"{savePath}, mClSize: {m}\nLinkage Method: {lm}, Num of Objects: {len(X)}"
                saveDendrogram = f"./FOSC Results/Dendrogram {savePath} - mClSize {m} - {lm}.png"

                # Plot results
                plotDendrogram(Z, partition, titlePlot, saveDendrogram)
                #plotDendrogram(Z, partition, titlePlot)

    return results

def generateDistanceMatrix(X, metric):
    # drop 'tracking_status'
    X = [np.array([s[1:] for s in record], dtype=np.double) for record in X]

    # get a sample to count the features (dimensions)
    n_dimensions = len(X[0][0])

    if metric == 'dtw':
        print(f"Producing distance matrix with dtw for {len(X)} series of {n_dimensions}-dimensions...")
        mat = dtw_ndim.distance_matrix_fast(X, n_dimensions)

    return mat