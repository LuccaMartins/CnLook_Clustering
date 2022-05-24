from Clustering_Framework.utils import *

import numpy as np

def analyzeRecords(records):
    #todo: change this function so that there are more records to find good clustering results.
    bad_records_idxs = []
    for i, record in enumerate(records):
        if not good_calibration(record[0]):
            print(f'The record {record[0]} will be dropped because its calibration was not good enough.')
        #getting count of stamps with untracked eyes
        both_untracked = list(record[1]['tracking_status'].values).count(1)
        right_untracked = list(record[1]['tracking_status'].values).count(2)
        left_untracked = list(record[1]['tracking_status'].values).count(3)
        # checking percentage of untracked eyes
        if (both_untracked*100)/len(record[1]) > 10 or \
           (right_untracked + both_untracked)*100/len(record[1]) > 15 or \
           (left_untracked + both_untracked)*100/len(record[1]) > 15:
            bad_records_idxs.append(i)
            print(f'The record {record[0]} will be dropped because of the number of stamps with untracked eyes'
                  f'. Both: {both_untracked}, right: {right_untracked}, left: {left_untracked}.')

    shift = 0
    for idx in bad_records_idxs:
        records.pop(idx - shift)
        shift += 1

    # X = selectFeatures(records, features)



    print(f"Size difference in timestamps: ")
    return records

def good_calibration(recording_id):
    print('build calibration analysis...')
    return True
