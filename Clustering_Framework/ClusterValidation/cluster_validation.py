import pandas as pd
import scipy.cluster.hierarchy
from sklearn import metrics
from validclust import dunn
import numpy as np
from Database.visualization import *
from Clustering_Framework.clustering_parameters import *
from scipy.spatial.distance import squareform
from scipy.stats import pointbiserialr
from sklearn.tree import DecisionTreeClassifier


def getClusterValidation(X, mat, partition):
    if set(partition).__contains__(-1): #checkinf if partition contains noise
        min = 3
    else:
        min = 2

    idx_to_remove = []
    for i, el in enumerate(partition):
        if el == -1:
            idx_to_remove.append(i)

    partition = np.delete(partition, idx_to_remove)
    X = np.delete(X, idx_to_remove, axis=0)
    mat = np.delete(np.delete(mat, idx_to_remove, axis=0), idx_to_remove, axis=1)

    if len(set(partition)) >= min:
        return {
            'Silhouette': metrics.silhouette_score(mat, partition, metric="precomputed"),
            # 'AUCC': computePBandAUCCIndexes(partition, mat),
            'Calinski-Harabasz Index': metrics.calinski_harabasz_score(X, partition),
            'David-Bouldin Index': metrics.davies_bouldin_score(X, partition),
            'Dunn Index': dunn(mat, partition)
        }
    else:
        return {
            'Error': '\nThe partition has a single cluster.\n'
        }

def build_decision_tree(result):
    Z = result['Method Info']['Hierarchy']
    n_clusters = len(set(result['Partition']))
    cut = scipy.cluster.hierarchy.cut_tree(Z, n_clusters=n_clusters)

    labels = list([i[0] for i in cut])
    labeled_data = pd.DataFrame(result['Data'], columns=subsets_of_features.get(result['Features Subset']))
    labeled_data['label'] = labels

    fig, axes = plt.subplots(nrows=1,
                            ncols=1,
                            figsize=(4, 4),
                            dpi=300)

    clf = DecisionTreeClassifier(random_state=1234)
    model = clf.fit(result['Data'], labels)

    sklearn.tree.plot_tree(model,
                           feature_names=labeled_data.columns,
                           filled=True,
                           class_names=True);

    plt.show()

def analyzeResults(allResults, rec_ids):
    bestResults = []
    thrs_best_silhouette = 0.75
    thrs_best_aucc = 0.7
    for i, result in enumerate(allResults):
        if 'Error' not in result['Cluster Validation'].keys():
            if result['Cluster Validation']['Silhouette'] >= thrs_best_silhouette:
                    # or result['Cluster Validation']['AUCC'] >= thrs_best_aucc:
                bestResults.append(result)
        else:
            print('No Cluster Validation for this result. Partition must be invalid.')
    print(f"\nNUMBER OF BEST RESULTS {len(bestResults)}, (thrs_best_silhouette = {thrs_best_silhouette}),"
          f" (thrs_best_silhouette = {thrs_best_aucc}")

    #Plotting scattered data with PCA
    for i, result in enumerate(bestResults):
        plot_scattered_data_PCA(result['Data'], rec_ids, result, savePlot=False, resultIdx=i)
        build_decision_tree(result)




    objects_pairwise, means1 = getObjectsPairwiseFrequency(bestResults, rec_ids)
    # objects_correlations, means2 = getObjectsCorrelationMatrix(bestResults, rec_ids)

    print('so what...')

    # >>>>>>>>>>>> RAND INDEX
    # pairwise_rand_scores = []
    # for A in [res['Partition'] for res in bestResults]:
    #     rand_scores = []
    #     for B in [res['Partition'] for res in bestResults]:
    #         print('Calculating rand_scores')
    #         rand_scores.append(metrics.rand_score(A, B))
    #     pairwise_rand_scores.append(rand_scores)

    return bestResults


def printBestSilhouettes(results):
    allSilhouettes_values = [col[3] for col in results]
    maxSilhouette = max(allSilhouettes_values)
    indexes = [i for i, x in enumerate(allSilhouettes_values) if x == maxSilhouette]

    for idx in indexes:
        print("Best Silhouette Validation: " + str(maxSilhouette) +
              " using minCSize = " + str(results[idx][0]) +
              ", and method = " + results[idx][1])


def computePBandAUCCIndexes(partition, distanceMatrix):
    noiseSize = 0
    for value in partition:
        if value == 0:
            noiseSize += 1

    penalty = (len(partition) - noiseSize) / len(partition)

    if (noiseSize == len(partition)): return np.nan, np.nan, noiseSize, penalty

    # dm = squareform(distanceMatrix)
    dm = distanceMatrix
    x = []
    yPointBiserial = []
    yAucc = []

    for i in range(len(partition) - 1):
        if partition[i] == 0: continue
        for j in range(i, len(partition)):
            if partition[j] == 0: continue
            yPointBiserial.append(dm[i, j])
            yAucc.append(1 / (1 + dm[i, j]))

            if partition[i] == partition[j]:
                x.append(1)
            else:
                x.append(0)

    # Compute internal validity index (point biserial)
    pb, pv = pointbiserialr(x, yPointBiserial)

    if any(label>1 for label in partition):
        # Compute area under the curve
        aucc = metrics.roc_auc_score(x, yAucc)
        return penalty * pb, penalty * aucc, noiseSize, penalty
    else:
        aucc = {'Error': 'Not a valid partition (only one cluster)'}
        return aucc


def getObjectsPairwiseFrequency(results, rec_ids):
    print('Getting objects pairwise frequency through partitions...')
    partitions = [result['Partition'] for result in results]

    all_objects_pairwiseCount = []
    for i in range(len(rec_ids)): #for each object

        object_pairwiseCount = np.zeros(len(rec_ids))
        for partition in partitions: #analyze each partition
            for j, label in enumerate(partition): #and get how many times each object is in the same cluster
                if label == partition[i]:
                    object_pairwiseCount[j] += 1
        all_objects_pairwiseCount.append(object_pairwiseCount)

    #dividing by the number of partitions to find the frequency
    all_objects_pairwiseFrequency = list(map(lambda x: x/len(results), all_objects_pairwiseCount))

    means = []
    for i in range(len(all_objects_pairwiseFrequency)):
        means.append(scipy.mean(all_objects_pairwiseFrequency[i]))

    print("Plotting pairwise frequency..")
    plt.figure(figsize=(30, 20))
    sns.heatmap(round(pd.DataFrame(all_objects_pairwiseFrequency), 2), cmap='flare', vmin=0, vmax=1)
    plt.title('Pairwise frequency', fontsize=80)
    plt.show()

    return all_objects_pairwiseFrequency, means


def getObjectsCorrelationMatrix(results, rec_ids):

    clusterings = pd.DataFrame([result['Partition'] for result in results])
    print("Getting objects correlation matrix")
    correlations = clusterings.corr()
    norm_correlations = pd.DataFrame(preprocessing.minmax_scale(correlations))
    means = []
    for i in range(len(correlations)):
        means.append(scipy.mean(correlations[i]))

    print("Plotting correlation matrix...")
    plt.figure(figsize=(30, 20))
    sns.heatmap(round(norm_correlations, 2), cmap='flare', vmin=0, vmax=1)
    plt.title('Correlation matrix', fontsize=80)
    plt.show()

    return norm_correlations, means