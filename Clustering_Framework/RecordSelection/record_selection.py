from Clustering_Framework.utils import *

import numpy as np

def analyzeRecords(records):
    # Selecting features from eye-tracker data
    features = ['tracking_status', 'left_x', 'left_y', 'right_x', 'right_y',
                'left_pupil_diameter_mm', 'right_pupil_diameter_mm']
    X = selectFeatures(records, features)

    # ... here I will analyze the consistency of the records, the size difference between the timeseries, etc...


    print(f"Size difference in timestamps: ")
    return X


#not sure if this function will be useful...
def selectFeatures(recordings, features):
    X_features = []
    for feature in features:
        X_features.append([np.array(rec[1][feature].values, dtype=np.double) for rec in recordings])
        # X_features.append(list(map(lambda x: np.array(x[1][feature].values, dtype=np.double), recordings)))

    result = []
    # for each recording
    for i in range(0, len(recordings)):
        # T.append(np.array([T_right_x[i], T_right_y[i], T_left_x, T_left_y]))
        values = []
        # for each stamp
        for j in range(0, len(recordings[i][1])):
            # values.append(np.array([T_right_x[i][j], T_right_y[i][j], T_left_x[i][j], T_left_y[i][j]]))
            valuesToAppend = []
            for feature_values in X_features:
                valuesToAppend.append(feature_values[i][j])
            values.append(np.array(valuesToAppend))
        result.append(np.array(values))
    return result