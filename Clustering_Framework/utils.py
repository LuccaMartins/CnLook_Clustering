import json
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

def getDistances_ToTarget(record, taskPositions, eye):
    recordPositions = list(zip(record[1][f'{eye}_x'].values, record[1][f'{eye}_y'].values))

    distancesToTarget = list(map(distance.euclidean, recordPositions, taskPositions))
    return distancesToTarget

def getSetOfSizes(recordings):
    return sorted(set([len(x) for x in recordings]))

#TODO: IMPROVE THIS FUNCTION BASED ON 'features_to_use'
def shapeFeaturedRecords(featuredRecords, features_to_use, eye='both'):
    X = []
    #IMPORTANT: ADpFF can't be used with other features.
    if features_to_use.__contains__('ADpFF'):
        if eye == 'both':
            print('Shaping records for both eyes...')
            record_features = []
            for record in list(featuredRecords['features'].values):
                for avrg_dist in record[0][f'ADpFF_left']:
                    record_features.append(avrg_dist)
                for avrg_dist in record[1][f'ADpFF_right']:
                    record_features.append(avrg_dist)
                X.append(record_features)
                record_features = []

        elif eye == 'left':
            print('Shaping records for left eye...')
            record_features = []
            for record in list(featuredRecords['features'].values):
                for avrg_dist in record[0][f'ADpFF_left']:
                    record_features.append(avrg_dist)
                X.append(record_features)
                record_features = []

        elif eye == 'right':
            print('Shaping records for right eye...')
            record_features = []
            for record in list(featuredRecords['features'].values):
                for avrg_dist in record[1][f'ADpFF_right']:
                    record_features.append(avrg_dist)
                X.append(record_features)
                record_features = []
    else:
        if eye == 'both':
            print('Shaping records for both eyes...')
            record_features = []
            for record in list(featuredRecords['features'].values):
                for feature in features_to_use:
                    record_features.append(record[0][f'{feature}_left'])
                    record_features.append(record[1][f'{feature}_right'])
                X.append(record_features)
                record_features = []

        elif eye == 'left':
            print('Shaping records for left eye...')
            record_features = []
            for record in list(featuredRecords['features'].values):
                for feature in features_to_use:
                    record_features.append(record[0][f'{feature}_left'])
                X.append(record_features)
                record_features = []

        elif eye == 'right':
            print('Shaping records for right eye...')
            record_features = []
            for record in list(featuredRecords['features'].values):
                for feature in features_to_use:
                    record_features.append(record[1][f'{feature}_right'])
                X.append(record_features)
                record_features = []

#TODO: use minmaxScaler
    X = preprocessing.minmax_scale(X)
    return X;

