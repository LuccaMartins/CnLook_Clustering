from hvl_code.analysis import *
from utils import *
from FOSC.util.fosc import FOSC

from dtaidistance import dtw, dtw_ndim
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn import metrics


def startFOSC():
    listOfMClSize = [2, 4, 5, 8, 16, 20, 30]
    methodsLinkage = ["single", "average", "ward", "complete", "weighted"]
    results = []
    allAUC = []

    for m in listOfMClSize:
        print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)

        for lm in methodsLinkage:
            titlePlot = "C&Look - " + Dict_Groups.get(groupId) + "(TaskId: " + taskId + "), mClSize: " + str(
                m) + "\nLinkage Method: " + lm + " , Num of Objects: " + str(len(X))
            savePath = "../FOSC/Results/" + Dict_Groups.get(groupId) + "(TaskId: " + taskId + "),\n mClSize: " + str(
                m) + "\n" + lm + ".png"
            saveDendrogram = "../FOSC/Results"  # Dendrogram " + dsGroupName + "(" + dsTaskName + "),\n mClSize=" + str(m) + "\n" + lm + ".png"

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

            # Plot results
            #plotPartition(X[:,0], X[:,1], partition, titlePlot)
            #plotDendrogram(Z, partition, titlePlot, saveDendrogram)
            #plotDendrogram(Z, partition, titlePlot)

    return results




#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "CnLook_DB")


#Reading records
groupId = "2"
taskId = "1003"
print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
records = list(getRecordings_ByTaskId(conn, groupId, taskId))


#Selecting features
features = ['left_x', 'left_y']
X = selectFeatures(records, features)

X = X[0:50]

#Calculating distance matrix with DTW
print(f"Producing distance matrix with dtw for {len(X)} series of {len(features)}-dimensions...")
mat = dtw_ndim.distance_matrix_fast(X, len(features))


#Start FOSC
results = startFOSC()


#Analyze FOSC results
printBestSilhouettes(results)




print(records)



