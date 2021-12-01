from analysis import *
import numpy as np
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
from FOSC.util.fosc import FOSC
from scipy.cluster.hierarchy import linkage, dendrogram


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
        return  #se for para salvar, não plota
    plt.show()



conn = connect_db("127.0.0.1","candlook_hvl")
dsGroupName = "Arusha"
dsTaskName = "Horizontal, 10 fixations"

allRecords = read_task_data(conn, dsGroupName, dsTaskName)
grouped = allRecords.groupby('recording_id')
listed = list(grouped)

X = []
for record in listed:
   X.append(list(record[1]['left_x'].values))


listOfMClSize = [4, 5, 8, 16, 20, 30]
methodsLinkage = ["single", "average", "ward", "complete", "weighted"]

# Running tests
for m in listOfMClSize:
    print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)

    for lm in methodsLinkage:
        titlePlot = "C&Look - " + dsGroupName + "(" + dsTaskName + "),\n mClSize=" + str(m) + "\n" + lm
        savePath = "../FOSC/Results/" + dsGroupName + "(" + dsTaskName + "),\n mClSize=" + str(m) + "\n" + lm + ".png"
        saveDendrogram = "../FOSC/Results/Dendrogram" + dsGroupName + "(" + dsTaskName + "),\n mClSize=" + str(m) + "\n" + lm + ".png"


        #normalizando só para rodar...
        min = 99999;
        X_norm = []
        for rec in X:
            if len(rec) < min: min = len(rec)
        for rec in X:
            X_norm.append(rec[0:min])

        print("Using linkage method %s" % lm)
        Z = linkage(X_norm, method=lm, metric="euclidean")

        foscFramework = FOSC(Z, mClSize=m)
        infiniteStability = foscFramework.propagateTree()
        partition = foscFramework.findProminentClusters(1, infiniteStability)

        # Plot results
        plotPartition(X_norm[:,0], X_norm[:,1], partition, titlePlot, savePath)
        plotDendrogram(Z, partition, titlePlot, saveDendrogram)








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

