from sklearn import metrics
from validclust import dunn

def getClusterValidation(X, mat, partition):
    if len(set(partition)) > 1:
        return {
            'Silhouette': metrics.silhouette_score(mat, partition, metric="precomputed"),
            'Calinski-Harabasz Index': metrics.calinski_harabasz_score(X, partition),
            'David-Bouldin Index': metrics.davies_bouldin_score(X, partition),
            'Dunn Index': dunn(mat, partition)
        }
    else:
        return {
            'Error': '\nThe partition has a single cluster.\n'
        }

def analyzeResults(allResults):
    best_silhouette = -1
    best_config_idx, best_method_idx, best_result_idx = -1, -1, -1
    for config_idx in range(0, len(allResults)):
        methods = allResults[config_idx]['Clustering Methods']
        for method_idx in range(0, len(methods)):
            result = methods[method_idx]['Results']
            for result_idx in range(0, len(result)):
                if not result[result_idx]['Cluster Validation'].__contains__('Error'):
                    if result[result_idx]['Cluster Validation']['Silhouette'] > best_silhouette:
                        best_silhouette = result[result_idx]['Cluster Validation']['Silhouette']
                        best_config_idx, best_method_idx, best_result_idx = config_idx, method_idx, result_idx
    # print(f'Best result for Silhouette Coeficient: \n{allResults[best_config_idx][best_method_idx][best_result_idx]}')

def printBestSilhouettes(results):
    allSilhouettes_values = [col[3] for col in results]
    maxSilhouette = max(allSilhouettes_values)
    indexes = [i for i, x in enumerate(allSilhouettes_values) if x == maxSilhouette]

    for idx in indexes:
        print("Best Silhouette Validation: " + str(maxSilhouette) +
              " using minCSize = " + str(results[idx][0]) +
              ", and method = " + results[idx][1])