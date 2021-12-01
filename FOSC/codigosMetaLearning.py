from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

from scipy.stats import pointbiserialr


from util.fosc import FOSC

import matplotlib.pyplot as plt
import numpy as np
import os

from random import shuffle

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler

import pandas as pd

import sys

palleteColors = ["#80ff72","#8af3ff","#7ee8fa","#89043d","#023c40","#c3979f","#797270","#c57b57", "#07004d","#0e7c7b",
                 "#c33149","#f49e4c", "#2e4057","#f2d7ee","#bfb48f","#a5668b","#002500","#720e07","#f46036","#78290f",
                 "#2a2b2a","#bb0a21","#7c99b4","#9a031e","#8f754f","#9ab87a","#f59ca9","#cb04a5","#993955","#3066be",
                 "#4c5760","#cf5c36","#d4afcd","#dfd5a5","#f374ae","#4fb0c6","#f2bac9","#8e936d","#a30b37","#85cb33"]

shuffle(palleteColors)


def plotPartition(x,y, result, title, saveDescription=None):
    uniqueValues = np.unique(result)
    
    fig = plt.figure(figsize=(15, 10))
    
    dicColors = {}
    dicColors[0] = "#000000"
    
    for  i in range(len(uniqueValues)):
        if uniqueValues[i] != 0:
            dicColors[uniqueValues[i]]= palleteColors[i]   
    
    
    for k, v in dicColors.items():
        plt.scatter(x[result==k], y[result==k], color=v )
    
    
    plt.title(title, fontsize=15)
    
    if saveDescription != None:
        plt.savefig(saveDescription)
        plt.close(fig)
        return
    
    plt.show() #\


def plotDendrogram(Z, result, ids=None, title=None, saveDescription=None):
    uniqueValues = np.unique(result)
    
    #print("Numero de clusters", len(uniqueValues))
    
    dicColors = {}
    dicColors[0] = "#000000"

    for i in range(len(uniqueValues)):
        if uniqueValues[i] != 0:
            dicColors[uniqueValues[i]]= palleteColors[i]    
    
    
    colorsLeaf={}
    for i in range(len(result)):
        colorsLeaf[i] = dicColors[result[i]]
    
    
    # notes:
    # * rows in Z correspond to "inverted U" links that connect clusters
    # * rows are ordered by increasing distance
    # * if the colors of the connected clusters match, use that color for link
    linkCols = {}
    for i, i12 in enumerate(Z[:,:2].astype(int)):
        c1, c2 = (linkCols[x] if x > len(Z) else colorsLeaf[x]
                  for x in i12)
                
        linkCols[i+1+len(Z)] = c1 if c1 == c2 else dicColors[0]
    
    fig = plt.figure(figsize=(25, 10))
    
    if ids.any()==None:
        dn = dendrogram(Z=Z, color_threshold=None, leaf_font_size=5,
                        leaf_rotation=45, link_color_func=lambda x: linkCols[x])
    else:
        dn = dendrogram(Z=Z, color_threshold=None, leaf_font_size=5, labels=ids,
                        leaf_rotation=45, link_color_func=lambda x: linkCols[x])
    
    
    plt.title(title, fontsize=12)
    
    
    if saveDescription != None:
        plt.savefig(saveDescription)
        plt.close(fig)
        return
    
    plt.show() #\


#### ############################################  Main script #########################################################


def computeGamma(partition, X):
        """
        Baker-Hubert Gamma Index: A measure of compactness, based on similarity between points in a cluster, compared to similarity
        with points in other clusters
        """
        XCopy = []
        partitionCopy=[]
        noiseSize=0
        
        for i in range(len(partition)):
            if partition[i] == 0:
                noiseSize+=1
            else:
                partitionCopy.append(partition[i])
                XCopy.append(X[i,:])
        
        if noiseSize==len(partition): return np.nan
        
        penalty = (len(partition)-noiseSize)/len(partition)
        
        XCopy = np.mat(XCopy)
        splus=0
        sminus=0
        pairDis=pdist(XCopy, "euclidean")
        numPair=len(pairDis)
        temp=np.zeros((len(partitionCopy),2))
        temp[:,0]=partitionCopy
        vecB=pdist(temp)
        
        #iterate through all the pairwise comparisons
        for i in range(numPair-1):
            for j in range(i+1,numPair):
                if vecB[i]>0 and vecB[j]==0:
                    #heter points smaller than homo points
                    if pairDis[i]<pairDis[j]:
                        splus=splus+1
                    #heter points larger than homo points
                    if pairDis[i]>vecB[j]:
                        sminus=sminus+1
                if vecB[i]==0 and vecB[j]>0:
                    #heter points smaller than homo points
                    if pairDis[j]<pairDis[i]:
                        splus=splus+1
                    #heter points larger than homo points
                    if pairDis[j]>vecB[i]:
                        sminus=sminus+1
        #compute the fitness
        validation = (splus-sminus)/(splus+sminus)
        
        return penalty*validation


def computePBandAUCCIndexes(partition, distanceMatrix):
    
    noiseSize = 0    
    for value in partition:
        if value==0:
            noiseSize+=1
    
    
    penalty = (len(partition)-noiseSize)/len(partition)
    
    if(noiseSize == len(partition)): return np.nan, np.nan, noiseSize, penalty

    dm =  squareform(distanceMatrix)
    
    x=[]
    yPointBiserial=[]
    yAucc = []
    
    for i in range(len(partition)-1):
        if partition[i] == 0: continue
        
        for j in range(i,len(partition)):
            if partition[j]==0: continue
            
            yPointBiserial.append(dm[i,j])
            yAucc.append(1/(1+dm[i,j]))
            
            if partition[i]==partition[j]:
                x.append(1)
            else:
                x.append(0)
    
    # Compute internal validity index (point biserial)
    pb,pv = pointbiserialr(x, yPointBiserial)
    
    # Compute area under the curve
    aucc = roc_auc_score(x, yAucc)
    
    return penalty*pb, penalty*aucc, noiseSize, penalty
    
    
    
def main():
    
    #pathFiles = "/home/jadson/Desktop/experiments/MetaDatasets/"
    pathFiles = sys.argv[1]
    
    listOfFiles    = os.listdir(pathFiles)
    
    listOfMClSize = [2,3,4,5,6,7,8,9,10]
    methodsLinkage = ["single", "average", "ward", "complete", "weighted"]
    numberOfFolds = [2,3,5]
    
    df = pd.DataFrame(columns=["dataset", "run", "NumberOfFolds", "fold", "linkage_method", "mClSize", "PBIndex", "AUCC", "GammaIndex", "Noise", "Penalty"])
    
    for fn in listOfFiles:
        if not fn.endswith(".csv"):continue
        
        varFileName = str(fn).rsplit(".", 1)[0]
        print ("\nPerforming experiments on dataset " + varFileName)
        
        # Creating folder with the dataset filename
        os.mkdir(pathFiles+varFileName)
    
        mat = np.genfromtxt(pathFiles+fn, dtype=float, delimiter=',', missing_values=np.nan, skip_header=1)[:, 1:]
        ids = np.genfromtxt(pathFiles+fn, dtype=int, delimiter=',', missing_values=np.nan, skip_header=1)[:, 0]
                
        for run in range(1,31):
            
            for nFold in numberOfFolds:
                kf = KFold(n_splits=nFold, shuffle=True)
                
                foldNumber = 0
                for trainIds, testIds in kf.split(mat):
                    trainSet    = mat[trainIds]
                    idsTrainSet = ids[trainIds]
                    foldNumber +=1
                    
                    # Scale training dataset to [0,1]                    
                    scaler   = MinMaxScaler().fit(trainSet)
                    trainSet = scaler.transform(trainSet)
                
                    dMatrix = pdist(trainSet, "euclidean")
                
                    # Running tests
                    for lm in methodsLinkage:
                        #print("--------------------------------------- Using linkage method %s ---------------------------------------" % lm)
                    
                        for m in listOfMClSize:
                            titlePlot = varFileName + "\n(" + lm + ", mClSize=" + str(m) + ", run=" + str(run) + " and fold=" + str(foldNumber) + ")"
                            saveDendrogram = pathFiles + "/" + varFileName +"/"+ lm +"-mclSize-"+str(m)+"-run-" + str(run) +"-fold" + str(foldNumber) + ".svg"
                        
                            #print("MClSize = %2d" % m)
                            Z= linkage(dMatrix, method=lm)
                        
                            foscFramework = FOSC(Z, mClSize=m)
                            infiniteStability = foscFramework.propagateTree()
                            partition = foscFramework.findProminentClusters(1,infiniteStability)
                        
                            pbIndex, auccIndex, noise, penalty = computePBandAUCCIndexes(partition, dMatrix)
                            gammaIndex = computeGamma(partition, trainSet)
                        
                            # Plot results
                            #plotPartition(mat[:,0], mat[:,1], partition, titlePlot, savePath)
                            plotDendrogram(Z, partition, idsTrainSet, titlePlot, saveDendrogram)
                        
                            # Update dataframe
                            df.loc[len(df)] = [varFileName, run, nFold, foldNumber, lm, m, pbIndex, auccIndex, gammaIndex, noise, penalty]
                            
         
                            
        # Save the dataframe
        df.to_csv(pathFiles+"/"+"dataframe-results.csv")
        
        
        
if __name__ == "__main__":
    main()