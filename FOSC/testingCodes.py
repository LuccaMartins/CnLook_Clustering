from scipy.cluster.hierarchy import linkage, dendrogram
from util.fosc import FOSC

from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import numpy as np
import os

from sklearn import datasets

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



#### ############################################  Main script #########################################################
pathFiles = "D:\Public Datasets\Wine"
listOfFiles = os.listdir(pathFiles)
# listOfFiles = [datasets.load_iris()]

listOfMClSize = [4, 5, 8, 16, 20, 30]
methodsLinkage = ["single", "average", "ward", "complete", "weighted"]
# methodsLinkage = ["weighted"]

for fn in listOfFiles:
    if not fn.endswith(".csv"):
        continue

    varFileName = str(fn).rsplit(".", 1)[0]
    print("\n\n\nPerforming experiments in dataset " + varFileName)

    if pathFiles.endswith('Wine'):
        mat0 = np.genfromtxt(pathFiles + "/" + fn, dtype=float, delimiter=',', missing_values=np.nan)
        mat = mat0[1:len(mat0)]
    elif pathFiles.endswith('Iris'):
        mat0 = np.genfromtxt(pathFiles + "/" + fn, dtype=float, delimiter=',', missing_values=np.nan)
        mat = mat0[1:len(mat0)]
        mat = mat[:,0:4]


    # Running tests
    for m in listOfMClSize:
        print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)

        for lm in methodsLinkage:
            titlePlot = varFileName + ", mClSize=" + str(m) + "\n" + lm
            savePath = pathFiles + "\FOSC Results/" + varFileName + "-" + lm + " mClSize=" + str(m) + ".png"
            saveDendrogram = pathFiles + "\FOSC Results/" + varFileName + "-dendrogram-" + lm + " mClSize-" + str(m) + ".png"

            print("Using linkage method %s" % lm)
            Z = linkage(mat, method=lm, metric="euclidean")

            foscFramework = FOSC(Z, mClSize=m)
            infiniteStability = foscFramework.propagateTree()
            partition = foscFramework.findProminentClusters(1, infiniteStability)

            # Plot results
            plotPartition(mat[:,0], mat[:,1], partition, titlePlot, savePath)
            plotDendrogram(Z, partition, titlePlot, saveDendrogram)

