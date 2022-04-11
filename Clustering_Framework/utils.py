import json

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

def getSetOfSizes(recordings):
    return sorted(set([len(x) for x in recordings]))












