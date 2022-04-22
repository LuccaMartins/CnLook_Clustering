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
