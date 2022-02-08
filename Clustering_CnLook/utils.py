import numpy as np

Dict_Groups = {
    '1'	:"default group",
    '2'	:"moivaro",
    '3'	:"Austevoll",
    '4'	:"tysnes",
    '5'	:"Arusha",
    '6'	:"moivaroIntellectuallyImpaired",
    '8'	:"ArushaPreTraining",
    '9'	:"ArushaPostTraining",
    '10' : "ArushaRescreening",
    '11' : "ArushaControl",
    '12' : "DAT"
}


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

def getSetOfSizes(recordings):
    return sorted(set([len(x) for x in recordings]))


def printBestSilhouettes(results):
    print(results)
    allSilhouettes_values = [col[2] for col in results]
    maxSilhouette = max(allSilhouettes_values)
    indexes = [i for i, x in enumerate(allSilhouettes_values) if x == maxSilhouette]

    for idx in indexes:
        print("Best Silhouette Validation: " + str(maxSilhouette) +
              " using minCSize = " + str(results[idx][0]) +
              ", and method = " + results[idx][1])



