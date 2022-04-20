from Clustering_Framework.utils import *

import numpy as np

def analyzeRecords(records):
    # Selecting features from eye-tracker data
    features = ['tracking_status', 'left_x', 'left_y', 'right_x', 'right_y',
                'left_pupil_diameter_mm', 'right_pupil_diameter_mm']

    bad_records_idxs = []
    for i in range(0, len(records)):
        #getting count of stamps with untracked eyes
        both_untracked = list(records[i][1]['tracking_status'].values).count(1)
        right_untracked = list(records[i][1]['tracking_status'].values).count(2)
        left_untracked = list(records[i][1]['tracking_status'].values).count(3)
        len_record = len(records[i][1])
        # checking percentage of untracked eyes
        if (both_untracked*100)/len_record > 10 or \
           (right_untracked*100)/len_record > 10 or \
           (left_untracked*100)/len_record > 10:
            bad_records_idxs.append(i)
            print(f'The record {records[i][0]} will be dropped because it has more than 10% '
                 f'of stamps with untracked eyes. Both: {both_untracked},'
                 f' right: {right_untracked}, left: {left_untracked}')

    shift = 0
    for idx in bad_records_idxs:
        records.pop(idx - shift)
        shift += 1

    # X = selectFeatures(records, features)



    print(f"Size difference in timestamps: ")
    return records


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