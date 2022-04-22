#TODO: add Silhouette and AUCC as validations
def analyzeResults(allResults):
    best_silhouette = -1
    best_config_idx, best_method_idx, best_result_idx = -1, -1, -1
    for config_idx in range(0, len(allResults)):
        methods = allResults[config_idx]['Clustering Methods']
        for method_idx in range(0, len(methods)):
            result = methods[method_idx]['Results']
            for result_idx in range(0, len(result)):
                if result[result_idx]['Silhouette'] > best_silhouette:
                    best_silhouette = result[result_idx]['Silhouette']
                    best_config_idx, best_method_idx, best_result_idx = config_idx, method_idx, result_idx


    print(f'{best_silhouette}')

def printBestSilhouettes(results):
    allSilhouettes_values = [col[3] for col in results]
    maxSilhouette = max(allSilhouettes_values)
    indexes = [i for i, x in enumerate(allSilhouettes_values) if x == maxSilhouette]

    for idx in indexes:
        print("Best Silhouette Validation: " + str(maxSilhouette) +
              " using minCSize = " + str(results[idx][0]) +
              ", and method = " + results[idx][1])