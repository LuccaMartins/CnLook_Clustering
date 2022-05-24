import operator
import scipy.cluster.hierarchy
from sklearn import metrics
from validclust import dunn
from Database.visualization import *
from scipy.stats import pointbiserialr
from DBCV import DBCV

def getClusterValidation(X, mat, partition):
    #Removing noisy elements for cluster validation
    idx_to_remove = []
    for i, el in enumerate(partition):
        if el == -1:
            idx_to_remove.append(i)
    partition_noNoise = np.delete(partition, idx_to_remove)
    X_noNoise = np.delete(X, idx_to_remove, axis=0)
    mat_noNoise = np.delete(np.delete(mat, idx_to_remove, axis=0), idx_to_remove, axis=1)

    penalty, noiseSize = getPenalty(partition)
    #todo: apply penalty for everyone but AUCC
    # https://www.dbs.ifi.lmu.de/~zimek/publications/SDM2014/DBCV.pdf usar para o DBSCAN
    if len(set(partition_noNoise)) >= 2:
        return {
            'Silhouette': penalty * round(metrics.silhouette_score(mat_noNoise, partition_noNoise, metric="precomputed"), 4),
            'AUCC': round(computePBandAUCCIndexes(partition, mat)[1], 4), #sends partition with noise because the function deals with it.
            'Calinski-Harabasz Index': penalty * round(metrics.calinski_harabasz_score(X_noNoise, partition_noNoise), 4),
            'David-Bouldin Index': penalty * round(metrics.davies_bouldin_score(X_noNoise, partition_noNoise), 4),
            'Dunn Index': penalty * round(dunn(mat_noNoise, partition_noNoise), 4),
            # 'DBCV': penalty * round(DBCV(X_noNoise, partition_noNoise), 4)
        }
    else:
        return {
            'Error': '\nThe partition has a single cluster.\n'
        }


#remover noiseeee para d dsd
def analyzeResults(allResults, rec_ids):
    bestResults = []
    thrs_best_silhouette = 0.75
    thrs_best_aucc = 0.7
    thrs_best_dbcv = 0.6
    for i, result in enumerate(allResults):
        if 'Error' not in result['Cluster Validation'].keys():
            if result['Cluster Validation']['Silhouette'] >= thrs_best_silhouette:
            # or result['Cluster Validation']['AUCC'] >= thrs_best_aucc:
            # or result['Cluster Validation']['DBCV'] >= thrs_best_dbcv:
                bestResults.append(result)
        else:
            print('No Cluster Validation for this result. Partition must be invalid.')
    print(f"\nNUMBER OF BEST RESULTS {len(bestResults)}, (thrs_best_silhouette = {thrs_best_silhouette}),"
          f" (thrs_best_silhouette = {thrs_best_aucc}")

    for i, result in enumerate(bestResults):
        plot_result(result, rec_ids, savePlot=True)
        # plot_scattered_data_PCA(result['Data'], rec_ids, result, savePlot=False, resultIdx=i)
        # plot_decision_tree(result)




    objects_pairwise, means = getObjectsPairwiseFrequency(bestResults, rec_ids)
    # objects_correlations, means2 = getObjectsCorrelationMatrix(bestResults, rec_ids)

    ordered = []

    sorted_pairs = sorted(enumerate(means), key=operator.itemgetter(1))
    sorted_pairs_ids = [(rec_ids[pair[0]], pair[1]) for pair in sorted_pairs]
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
    penalty, noiseSize = getPenalty(partition)

    if (noiseSize == len(partition)): return np.nan, np.nan, noiseSize, penalty

    # dm = squareform(distanceMatrix)
    dm = distanceMatrix
    x = []
    yPointBiserial = []
    yAucc = []

    for i in range(len(partition) - 1):
        if partition[i] == -1: continue
        for j in range(i, len(partition)):
            if partition[j] == -1: continue
            yPointBiserial.append(dm[i, j])
            yAucc.append(1 / (1 + dm[i, j]))

            if partition[i] == partition[j]:
                x.append(1)
            else:
                x.append(0)

    # Compute internal validity index (point biserial)
    pb, pv = pointbiserialr(x, yPointBiserial)
    set_partition = set(partition)
    if (set_partition.__contains__(-1) and len(set_partition) >= 3)\
    or (not set_partition.__contains__(-1) and len(set_partition) >= 2):
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


def getPenalty(partition):
    noiseSize = 0
    for value in partition:
        if value == -1:
            noiseSize += 1

    penalty = (len(partition) - noiseSize) / len(partition)
    return penalty, noiseSize