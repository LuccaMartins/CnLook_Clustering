import json
import scipy
from matplotlib.pyplot import sci
from scipy.spatial import distance
from sklearn import preprocessing

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

def columnsForBothEyes(features):
    features_both_eyes = []
    for feature in features:
        if feature == 'ADB':
            features_both_eyes.append(f'{feature}')
        else:
            features_both_eyes.append(f'{feature}_left')
            features_both_eyes.append(f'{feature}_right')

    return features_both_eyes



def normalizeTimestamps(timestamps):
    normalized = [0]
    for i in range(1, len(timestamps)):
        normalized.append(normalized[i-1] + timestamps[i]/1000 - timestamps[i-1]/1000)
    return normalized

def getTaskPositions(task, timestamps):
    #TODO: this function must be different depending on the parameter_type of the task.
    # i.e., finding task position for Fixation Tasks is different from Smooth Pursuit Tasks, because
    # the positions are store differently in the database.

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

def getDistances_betweenEyes(record):
    rightPositions = list(zip(record[1][f'right_x'].values, record[1][f'right_y'].values))
    leftPositions = list(zip(record[1][f'left_x'].values, record[1][f'left_y'].values))
    distancesBetween = list(map(distance.euclidean, rightPositions, leftPositions))
    return distancesBetween


def getDistances_ToTarget(record, taskPositions, eye, last_valid_idx):
    record_valid_Positions = list(zip(record[1][f'{eye}_x'].values, record[1][f'{eye}_y'].values))[:last_valid_idx]
    distancesToTarget = list(map(distance.euclidean, record_valid_Positions, taskPositions))
    return distancesToTarget

def getSetOfSizes(recordings):
    return sorted(set([len(x) for x in recordings]))

def shapeFeaturedRecords_ADpFF(featuredRecords, features_to_use, eye='both'):
    # getting mean for means of fixations in right and left side of the screen
    X = []
    if eye == 'both':
        print('Shaping records for both eyes...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADpFF':
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][0:5]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][5:10]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][10:15]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][15:20]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][20:25]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][25:30]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][0:5]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][5:10]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][10:15]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][15:20]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][20:25]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][25:30]))
                    record_features.append(scipy.mean(record[0][f'ADpFF_left'][0:5] + record[0][f'ADpFF_left'][10:15] + record[0][f'ADpFF_left'][20:25]))
                    record_features.append(scipy.mean(record[0][f'ADpFF_left'][5:10] + record[0][f'ADpFF_left'][15:20] + record[0][f'ADpFF_left'][25:30]))
                    record_features.append(scipy.mean(record[1][f'ADpFF_right'][0:5] + record[1][f'ADpFF_right'][10:15] + record[1][f'ADpFF_right'][20:25]))
                    record_features.append(scipy.mean(record[1][f'ADpFF_right'][5:10] + record[1][f'ADpFF_right'][15:20] + record[1][f'ADpFF_right'][25:30]))
                else:
                    if feature == 'ADB':
                        record_features.append(record[2][f'{feature}'])
                    else:
                        record_features.append(record[0][f'{feature}_left'])
                        record_features.append(record[1][f'{feature}_right'])

                    # for avrg_dist in record[0][f'ADpFF_left']:
                    #     record_features.append(avrg_dist)
                    # for avrg_dist in record[1][f'ADpFF_right']:
                    #     record_features.append(avrg_dist)
            X.append(record_features)
            record_features = []

    elif eye == 'left':
        print('Shaping records for left eye...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADpFF':
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][0:5]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][5:10]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][10:15]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][15:20]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][20:25]))
                    # record_features.append(scipy.mean(record[0][f'ADpFF_left'][25:30]))
                    record_features.append(scipy.mean(
                        record[0][f'ADpFF_left'][0:5] + record[0][f'ADpFF_left'][10:15] + record[0][f'ADpFF_left'][20:25]))
                    record_features.append(scipy.mean(
                        record[0][f'ADpFF_left'][5:10] + record[0][f'ADpFF_left'][15:20] + record[0][f'ADpFF_left'][25:30]))
                else:
                    if feature == 'ADB':
                        record_features.append(record[2][f'{feature}'])
                    else:
                        record_features.append(record[0][f'{feature}_left'])
            # for avrg_dist in record[0][f'ADpFF_left']:
            #     record_features.append(avrg_dist)
            X.append(record_features)
            record_features = []

    elif eye == 'right':
        print('Shaping records for right eye...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADpFF':
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][0:5]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][5:10]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][10:15]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][15:20]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][20:25]))
                    # record_features.append(scipy.mean(record[1][f'ADpFF_right'][25:30]))
                    record_features.append(scipy.mean(
                        record[0][f'ADpFF_left'][0:5] + record[0][f'ADpFF_left'][10:15] + record[0][f'ADpFF_left'][20:25]))
                    record_features.append(scipy.mean(
                        record[0][f'ADpFF_left'][5:10] + record[0][f'ADpFF_left'][15:20] + record[0][f'ADpFF_left'][25:30]))

                else:
                    if feature == 'ADB':
                        record_features.append(record[2][f'{feature}'])
                    else:
                        record_features.append(record[1][f'{feature}_right'])

            # for avrg_dist in record[1][f'ADpFF_right']:
            #     record_features.append(avrg_dist)
            X.append(record_features)
            record_features = []


    X = preprocessing.minmax_scale(X)
    return X



def shapeFeaturedRecords(featuredRecords, features_to_use, eye):
    if features_to_use.__contains__('ADpFF'):
        return shapeFeaturedRecords_ADpFF(featuredRecords, features_to_use, eye)

    X = []
    if eye == 'both':
        print('Shaping records for both eyes...')
        record_features = []
        for record in list(featuredRecords['features'].values):
            for feature in features_to_use:
                if feature == 'ADB':
                    record_features.append(record[2][f'{feature}'])
                else:
                    record_features.append(record[0][f'{feature}_left'])
                    record_features.append(record[1][f'{feature}_right'])

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

