import json
from turtle import right

import scipy
from matplotlib.pyplot import sci
from pyexpat import features
from scipy.spatial import distance
from sklearn import preprocessing
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
import itertools
from itertools import combinations
from Database.visualization import *


Dict_Groups = {
    '1': "default group",
    '2': "moivaro",
    '3': "Austevoll",
    '4': "tysnes",
    '5': "Arusha",
    '6': "moivaroIntellectuallyImpaired",
    '8': "ArushaPreTraining",
    '9': "ArushaPostTraining",
    '10': "ArushaRescreening",
    '11': "ArushaControl",
    '12': "DAT"
}





def normalizeTimestamps(timestamps):
    normalized = [0]
    for i in range(1, len(timestamps)):
        normalized.append(normalized[i-1] + timestamps[i]/1000 - timestamps[i-1]/1000)
    return normalized


def getTaskPositions(task, timestamps):
    # this function would be different depending on the parameter_type of the task.

    # timestamps = normalizeTimestamps(timestamps)
    normalized_Positions = json.loads(task.animation_blueprint.values[0])['NormalizedPositionDurations']
    parameter_data = json.loads(task.parameter_data.values[0])
    taskPositions = []

    if task.parameter_type.values[0] == 'StandardAnimationParameters':

        if parameter_data['FixationsPerLine'] == 0:
            # it's Smooth Pursuit task. There may be differences for dealing with data of
            # horizontal/vertical and diagonal tasks.
            print('preparing for getting task positions...')

        elif parameter_data['FixationsPerLine'] > 0:
            for timestamp in timestamps:
                for i in range(0, len(normalized_Positions) - 1):
                    if normalized_Positions[i]['DurationSoFarInMs'] <= timestamp < normalized_Positions[i + 1]['DurationSoFarInMs']:
                        x, y = normalized_Positions[i]['ToPoint'].split(',')
                        taskPositions.append([float(x), float(y)])
                        break

    elif task.parameter_type.values[0] == 'SaccadeSpeedTestParameters' or\
         task.parameter_type.values[0] == 'WordGridTaskJson' or\
         task.parameter_type.values[0] == 'ReadingTaskJson':

        print(f"ERROR: Can't get figure positions for this parameter type: {task.parameter_type}")
        return None

    return taskPositions


# Use only stamps with both eyes tracked
def getDistances_betweenEyes(record):
    distancesBetween = []
    for i in range(len(record[1]['timestamp'].values)):
        if record[1]['tracking_status'].values[i] == 0:
            right = [record[1]['right_x'].values[i], record[1]['right_y'].values[i]]
            left = [record[1]['left_x'].values[i], record[1]['left_y'].values[i]]
            distancesBetween.append(distance.euclidean(right, left))
    return distancesBetween


def getDistances_ToTarget(record, taskPositions, eye, eyeTracked=False):
    last_valid_idx = len(taskPositions)
    record_valid_Positions = list(zip(record[1][f'{eye}_x'].values, record[1][f'{eye}_y'].values))[:last_valid_idx]
    distancesToTarget = []

    if eyeTracked == True:
        for i in range(last_valid_idx):
            if (eye == 'left' and record[1]['tracking_status'].values[i] not in [1, 3]) or \
               (eye == 'right' and record[1]['tracking_status'].values[i] not in [1, 2]):
                distancesToTarget.append(distance.euclidean(record_valid_Positions[i], taskPositions[i]))
    else:
        for i in range(last_valid_idx):
                distancesToTarget.append(distance.euclidean(record_valid_Positions[i], taskPositions[i]))

    return distancesToTarget

def getBestFeatures(corr):
    upper_tri = corr.where(np.triu(np.ones(corr.shape), k=1).astype(np.bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.8)]

    best_features = []
    for column in upper_tri.columns:
        if column not in to_drop:
            best_features.append(column)

    return best_features


def createSubsetOfFeatures_bothEyes(featuredRecords):
    data = []
    for record_values in featuredRecords['features'].values:
        data.append(record_values[0] | record_values[1] | record_values[2])

    df = pd.DataFrame(data)

    # drop saccades count
    df = df.drop(f'SC_left', axis=1)
    df = df.drop(f'SC_right', axis=1)

    # df = df.drop(f'FDMax_{eye}', axis=1)
    # df = df.drop(f'FDMin_{eye}', axis=1)

    plotCorrelationMatrix(df)

    all_features = [f'FC_left', f'AFD_left', f'AFDisp_left', f'AFDispH_left', f'AFDispV_left',
                    f'ASD_left', f'ASA_left', f'SAMax_left', f'ADTF_left', f'SPL_left',
                    f'ADT_left', f'ADTL_left', f'ADTR_left', f'ADFF_left', f'FC_right',
                    f'AFD_right', f'AFDisp_right', f'AFDispH_right', f'AFDispV_right',
                    f'ASD_right', f'ASA_right', f'SAMax_right', f'ADTF_right', f'SPL_right',
                    f'ADT_right', f'ADTL_right', f'ADTR_right', f'ADFF_right', f'ADB']
    subsets = []
    for feature in all_features:
        corr = list(df.corr()[feature])
        sorted_corr = sorted(corr)
        sorted_idxs = []

        for i in range(4):
            sorted_idxs.append(df.keys()[corr.index(sorted_corr[i])])

        for i in range(2, 6):
            combs = list(combinations(sorted_idxs, i-1))
            for comb in combs:
                newSubset = [feature] + list(comb)
                subsets.append(sorted(newSubset))

    subsets = removeDuplicates(subsets)

    return sorted(subsets, key=len)


def createSubsetsOfFeatures(featuredRecords, eye):
    if eye == 'both':
        return createSubsetOfFeatures_bothEyes(featuredRecords)

    data = []
    if eye == 'left':
        for record_values in featuredRecords['features'].values:
            data.append(record_values[0] | record_values[2])
    elif eye == 'right':
        for record_values in featuredRecords['features'].values:
            data.append(record_values[1] | record_values[2])

    df = pd.DataFrame(data)

    # drop saccades count
    df = df.drop(f'SC_{eye}', axis=1)
    # df = df.drop(f'FDMax_{eye}', axis=1)
    # df = df.drop(f'FDMin_{eye}', axis=1)

    plotCorrelationMatrix(df)

    all_features = [f'FC_{eye}', f'AFD_{eye}', f'AFDisp_{eye}', f'AFDispH_{eye}', f'AFDispV_{eye}',
                    f'ASD_{eye}', f'ASA_{eye}', f'SAMax_{eye}', f'ADTF_{eye}', f'SPL_{eye}',
                    f'ADT_{eye}', f'ADTL_{eye}', f'ADTR_{eye}', f'ADFF_{eye}', f'ADB']
    subsets = []
    for feature in all_features:
        corr = list(df.corr()[feature])
        sorted_corr = sorted(corr)
        sorted_idxs = []

        for i in range(4):
            sorted_idxs.append(df.keys()[corr.index(sorted_corr[i])].split('_')[0])

        for i in range(2, 6):
            combs = list(combinations(sorted_idxs, i-1))
            for comb in combs:
                newSubset = [feature.split('_')[0]] + list(comb)
                subsets.append(sorted(newSubset))

    subsets = removeDuplicates(subsets)

    return sorted(subsets, key=len)

def removeDuplicates(subsets):
    subsets.sort()
    return list(subset for subset, _ in itertools.groupby(subsets))



def shapeFeaturedRecords(featuredRecords, features_to_use, eye):
    X = []
    if eye == 'both':
        print('Shaping records for both eyes...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADB':
                    record_features.append(record[2][f'{feature}'])
                else:
                    if feature.split('_')[1] == 'left':
                        record_features.append(record[0][f'{feature}'])
                    elif feature.split('_')[1] == 'right':
                        record_features.append(record[1][f'{feature}'])
            X.append(record_features)
            record_features = []
    elif eye == 'left':
        print('Shaping records for left eye...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADB':
                    record_features.append(record[2][f'{feature}'])
                else:
                    record_features.append(record[0][f'{feature}_left'])
            X.append(record_features)
            record_features = []
    elif eye == 'right':
        print('Shaping records for right eye...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADB':
                    record_features.append(record[2][f'{feature}'])
                else:
                    record_features.append(record[1][f'{feature}_right'])
            X.append(record_features)
            record_features = []

    X = preprocessing.minmax_scale(X)
    return X;

