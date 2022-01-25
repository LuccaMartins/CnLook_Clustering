import pandas

from analysis import *
import numpy as np
import array
import matplotlib.pyplot as plt
import collections, numpy
import psycopg2
import pandas as pd
import scipy.interpolate
import scipy.stats
import scipy.signal
import ast
import sklearn.decomposition
from sklearn.base import BaseEstimator, TransformerMixin
import matplotlib.pyplot as plt
import re
from pandas import DataFrame
from matplotlib.pyplot import figure
import plottingRecords as plotting
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from scipy.spatial.distance import euclidean
from scipy.stats import pointbiserialr

# from dtw import *
from dtaidistance import dtw, dtw_ndim
from dtaidistance import dtw_visualisation as dtwvis
from FOSC.util.fosc import FOSC
from scipy.cluster.hierarchy import linkage, dendrogram

# plt.style.use("ggplot")

palleteColors = ["#80ff72", "#8af3ff", "#7ee8fa", "#89043d", "#023c40", "#c3979f", "#797270", "#c57b57", "#07004d",
                 "#0e7c7b", "#c33149", "#f49e4c", "#2e4057", "#f2d7ee", "#bfb48f", "#a5668b", "#002500", "#720e07",
                 "#f46036", "#78290f"]

def plotPartition(x, y, result, title, saveDescription=None):
    uniqueValues = np.unique(result)

    fig = plt.figure(figsize=(10, 5))

    dicColors = {}
    dicColors[0] = "#000000"

    for i in range(len(uniqueValues)):
        if uniqueValues[i] != 0:
            dicColors[uniqueValues[i]] = palleteColors[i]

    for k, v in dicColors.items():
        plt.scatter(x[result == k], y[result == k], color=v)

    plt.title(title, fontsize=15)

    if saveDescription != None:
        plt.savefig(saveDescription)
        plt.close(fig)
        return  #se for para salvar, não plota
    plt.show()

def plotDendrogram(Z, result, title, saveDescription=None):
    uniqueValues = np.unique(result)

    dicColors = {}
    dicColors[0] = "#000000"

    for i in range(len(uniqueValues)):
        if uniqueValues[i] != 0:
            dicColors[uniqueValues[i]] = palleteColors[i]

    colorsLeaf = {}
    for i in range(len(result)):
        colorsLeaf[i] = dicColors[result[i]]

    # notes:
    # * rows in Z correspond to "inverted U" links that connect clusters
    # * rows are ordered by increasing distance
    # * if the colors of the connected clusters match, use that color for link
    linkCols = {}
    for i, i12 in enumerate(Z[:, :2].astype(int)):
        c1, c2 = (linkCols[x] if x > len(Z) else colorsLeaf[x]
                  for x in i12)

        linkCols[i + 1 + len(Z)] = c1 if c1 == c2 else dicColors[0]

    fig = plt.figure(figsize=(10, 5))

    dn = dendrogram(Z=Z, color_threshold=None, leaf_font_size=5,
                    leaf_rotation=45, link_color_func=lambda x: linkCols[x])
    plt.title(title, fontsize=12)

    if saveDescription != None:
        plt.savefig(saveDescription)
        plt.close(fig)
        return

    plt.show()

def plotWarpingExamples(X, n):
    for i in range(0, n):
        path = dtw.warping_path(X[i], X[i+n])
        dtwvis.plot_warping(X[i], X[i+n], path, filename="warp" + str(i) + ".png")




    #  MAIN CODE   =========================================================================================================

def selectFeatures(recordings, features):

    X_features = []
    for feature in features:
        X_features.append(list(map(lambda x: np.array(x[1][feature].values, dtype=np.double), recordings)))

    result = []
    # for each recording
    for i in range(0, len(recordings)):
        # T.append(np.array([T_right_x[i], T_right_y[i], T_left_x, T_left_y]))
        values = []
        #for each stamp
        for j in range(0, len(recordings[i][1])):
            # values.append(np.array([T_right_x[i][j], T_right_y[i][j], T_left_x[i][j], T_left_y[i][j]]))
            valuesToAppend = []
            for feature_values in X_features:
                valuesToAppend.append(feature_values[i][j])
            values.append(np.array(valuesToAppend))
        result.append(np.array(values))
    return result

def pairwiseClustering(partition):
    n = len(partition)
    mat = np.zeros((n, n))

    #computing only the elements above the diagonal
    for i in range(0, n):
        for j in range(i, n):
            if i == j:
                mat[i][j] = 1
                mat[j][i] = 1
            else:
                if partition[i] == partition[j]:
                    mat[i][j] = 1
                    mat[j][i] = 1

    return mat


def computePBandAUCCIndexes(partition, distanceMatrix):
    noiseSize = 0
    for value in partition:
        if value == 0:
            noiseSize += 1

    penalty = (len(partition) - noiseSize) / len(partition)

    if (noiseSize == len(partition)): return np.nan, np.nan, noiseSize, penalty

    # dm = squareform(distanceMatrix)
    dm = distanceMatrix
    print(dm.shape)
    x = []
    yPointBiserial = []
    yAucc = []

    for i in range(len(partition) - 1):
        if partition[i] == 0: continue

        for j in range(i, len(partition)):
            if partition[j] == 0: continue

            yPointBiserial.append(dm[i, j])
            yAucc.append(1 - dm[i, j])

            if partition[i] == partition[j]:
                x.append(1)
            else:
                x.append(0)

    # Compute internal validity index (point biserial)
    pb, pv = pointbiserialr(x, yPointBiserial)

    # Compute area under the curve
    aucc = roc_auc_score(x, yAucc)

    return penalty * pb, penalty * aucc, noiseSize, penalty

print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "candlook_hvl")

dsGroupName = "moivaro"
dsTaskName = "Horizontal"
print('Reading records from database: ' + dsGroupName + " - " + dsTaskName)
allRecords = read_task_data(conn, dsGroupName, dsTaskName)

#Grouping the samples by id
grouped = allRecords.groupby('recording_id')


#stamps content: timestamp,
#                left_pupil_diameter_mm,
#                right_pupil_diameter_mm,
#                left_x, left_y,
#                right_x, right_y
features = ['left_x']
X = selectFeatures(list(grouped), features)
print('set: ')
print(sorted(set([len(x) for x in X])))
#plotting.plotTimeSeries(list(grouped)[0][0], 'left_x', X[0])

# X = X[30:70]

# print("Saving warping examples...")
# plotWarpingExamples(X, 10)

print("Producing distance matrix with dtw for " + str(len(X)) + " series of " + str(len(features)) + "-dimensions...")
mat = dtw_ndim.distance_matrix_fast(X, len(features))


listOfMClSize = [2, 4, 5, 8, 16, 20, 30]
methodsLinkage = ["single", "average", "ward", "complete", "weighted"]

allSilhouettes = []
allAUC = []
# Running tests
for m in listOfMClSize:
    print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)

    for lm in methodsLinkage:
        titlePlot = "C&Look - " + dsGroupName + "(" + dsTaskName + "), mClSize: " + str(m) + "\nLinkage Method: " + lm + " , Num of Objects: " + str(len(X))
        savePath = "../FOSC/Results/" + dsGroupName + "(" + dsTaskName + "),\n mClSize: " + str(m) + "\n" + lm + ".png"
        saveDendrogram = "../FOSC/Results" #Dendrogram " + dsGroupName + "(" + dsTaskName + "),\n mClSize=" + str(m) + "\n" + lm + ".png"


        print("Calling linkage with " + lm + " passing the distances matrix...")
        Z = linkage(mat, method=lm)

        foscFramework = FOSC(Z, mClSize=m)
        infiniteStability = foscFramework.propagateTree()
        partition = foscFramework.findProminentClusters(1, infiniteStability)

        # validação do algoritmo: silhouette ou AUC Under Curve
        if len(set(partition)) > 1:
            silhouette = metrics.silhouette_score(mat, partition, metric="precomputed")
            allSilhouettes.append([m, lm, silhouette])

            # pairwise_clustering = pairwiseClustering(partition)
            # fpr, tpr, thresholds = metrics.roc_curve(partition, pairwise_clustering, pos_label=2)
            # allAUC.append(metrics.auc(fpr, tpr))

            a, b, c, d = computePBandAUCCIndexes(partition, mat)
        else:
            allSilhouettes.append([m, lm, -1])


        #descrever o cluster

        # Plot results
        #plotPartition(X[:,0], X[:,1], partition, titlePlot)
        #plotDendrogram(Z, partition, titlePlot, saveDendrogram)
        #plotDendrogram(Z, partition, titlePlot)

print(allSilhouettes)
allSilhouettes_values = [col[2] for col in allSilhouettes]
maxSilhouette = max(allSilhouettes_values)
indexes = [i for i, x in enumerate(allSilhouettes_values) if x == maxSilhouette]

for idx in indexes:
    print("Best Silhouette Validation: " + str(maxSilhouette) +
      " using minCSize = " + str(allSilhouettes[idx][0]) +
      ", and method = " + allSilhouettes[idx][1])



#
# max_time=max(time)
# min_time=min(time)
# tt=(max_time-min_time)*1000
# #print(time)
#
# plt.plot(time, positions_x['right_x'], color='b', label='Right Eye')
#
# # Plot another line on the same chart/graph
# plt.plot(time, positions_x['left_x'], color='r', label='Left Eye')
#
# plt.legend()
# plt.show()

