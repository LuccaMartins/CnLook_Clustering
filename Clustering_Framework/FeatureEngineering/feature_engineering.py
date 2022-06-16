from Clustering_Framework.EventDetection.event_Detection import *
from Clustering_Framework.utils import *
from Database.visualization import *

from scipy.spatial import distance
import pandas as pd
import scipy


def createFeaturedRecords(task, records):
    print('Starting feature engineering...')
    parameter_data = json.loads(task.parameter_data.values[0])

    if parameter_data['FixationsPerLine'] > 0:
        featured_records = features_task_with_fixations_EMA(task, records)
    else:
        print('Features not ready for smooth pursuit tasks...')

    return featured_records

def features_path_length(record, eye):
    x = record[1][f'{eye}_x'].values
    y = record[1][f'{eye}_y'].values
    path_length = 0
    last_tracked = -1
    for i in range(1, len(record[1])):
        if (eye == 'left' and record[1]['tracking_status'].values[i] not in [1, 3]) or \
           (eye == 'right' and record[1]['tracking_status'].values[i] not in [1, 2]):
            if last_tracked == -1:
                path_length += distance.euclidean([x[i-1],y[i-1]], [x[i],y[i]])
            else:
                path_length += distance.euclidean([x[last_tracked], y[last_tracked]], [x[i], y[i]])
                last_tracked = -1
        else:
            if last_tracked == -1:
                last_tracked = i-1

    return path_length


def features_event_latency(movements):
    latencies = []
    event_beginnings = [range[0] for range in [movement['Range'] for movement in movements]]
    event_endings = [range[1] for range in [movement['Range'] for movement in movements]]

    for i in range(1, len(event_beginnings)):
        latencies.append(event_beginnings[i] - event_endings[i-1] - 1)

    average_latency = scipy.mean(latencies)
    # if pd.isna(average_latency):
    #     average_latency = 0

    return average_latency


def features_event_velocity(movements):
    # TODO: needs the last point of the last movement and the first point of the next movement
    print('[WARNING] Feature not developed yet...')


def features_event_amplitude(movements):
    # TODO: needs the last point of the last movement and the first point of the next movement
    print('[WARNING] Feature not developed yet...')


def features_event_dispersion(movements):
    # movements_positions = [movements[i]['Positions'] for i in range(0, len(movements))]
    dispersions = []
    total_disp_x = 0
    total_disp_y = 0
    for movement in movements:
        x_values = [pos[0] for pos in movement]
        y_values = [pos[1] for pos in movement]
        disp_x = max(x_values) - min(x_values)
        disp_y = max(y_values) - min(y_values)
        # dispersions.append({'disp_x': disp_x,
        #                     'disp_y': disp_y})
        total_disp_x += disp_x
        total_disp_y += disp_y

    # total_disp = scipy.mean([total_disp_x, total_disp_y])
    average_horizontal_disp = total_disp_x/len(movements)
    average_vertical_disp = total_disp_y/len(movements)
    average_disp = (average_horizontal_disp + average_vertical_disp)/2
    return average_disp, average_horizontal_disp, average_vertical_disp


def features_event_duration(movements):
    ranges = [movements[i]['Range'] for i in range(0, len(movements))]
    durations = [range[1] - range[0] + 1 for range in ranges]
    average = scipy.mean(durations)

    if not durations:
        print('PROBLEM: List of movements is empty for this record...')
        return average, 0, 0

    return average, max(durations), min(durations)


def features_task_with_fixations_EMA(task, records):
    features = []
    featured_records = []
    for record in records:
        print(f'\n-----> Extracting features from record {record[0]}')
        # records have different sizes...
        taskPositions = getTaskPositions(task, normalizeTimestamps(record[1]['timestamp'].array))
        shouldAddRecord = True
        for eye in 'left', 'right':
            (saccades, fixations, centroids, centroids_count, fixations_ranges) = \
                identify_events_ema(record, eye, last_valid_idx=len(taskPositions)-1)

            valid_fixations_ranges = []
            for fix_range in fixations_ranges:
                if fix_range[1] < len(taskPositions) - 1:
                    valid_fixations_ranges.append(fix_range)

            if len(saccades) < 2 or \
               len(fixations) < 2 or \
               len(centroids) < 2 or \
               len(valid_fixations_ranges) < 2:
                shouldAddRecord = False
            else:
                distancesToTarget = getDistances_ToTarget(record, taskPositions, eye)
                distancesToTarget_valid = getDistances_ToTarget(record, taskPositions, eye, eyeTracked=True)
                (AFDisp, AFDispH, AFDispV) = features_event_dispersion(fixations)
                (ADpFF, ADTL, ADTR, ADFF) = features_avg_dist_figFixations(record, taskPositions, eye)

                features.append({
                                 f'FC_{eye}': len(fixations),
                                 f'ADTF_{eye}': scipy.mean([scipy.mean(distancesToTarget[fix[0]:fix[1]+1]) for fix in valid_fixations_ranges]),
                                 f'AFD_{eye}': scipy.mean([len(x) for x in fixations]),
                                 # f'FDMax_{eye}': max([len(x) for x in fixations]),
                                 # f'FDMin_{eye}': min([len(x) for x in fixations]),
                                 f'AFDisp_{eye}': AFDisp,
                                 f'AFDispH_{eye}': AFDispH,
                                 f'AFDispV_{eye}': AFDispV,
                                 f'SC_{eye}': len(saccades),
                                 f'ASD_{eye}': scipy.mean([len(x) for x in saccades]),
                                 # f'SDMax_{eye}': max([len(x) for x in saccades]),
                                 # f'SDMin_{eye}': min([len(x) for x in saccades]),
                                 f'SPL_{eye}': features_path_length(record, eye),
                                 f'ASA_{eye}': scipy.mean([distance.euclidean(saccade[0], saccade[-1]) for saccade in saccades]),
                                 f'SAMax_{eye}': max([distance.euclidean(saccade[0], saccade[-1]) for saccade in saccades]),
                                 # f'SAMin_{eye}': min([distance.euclidean(saccade[0], saccade[-1]) for saccade in saccades]),
                                 f'ADT_{eye}': scipy.mean(distancesToTarget),
                                 # f'ADpFF_{eye}': ADpFF, #same as ADT
                                 f'ADTL_{eye}': ADTL,
                                 f'ADTR_{eye}': ADTR,
                                 f'ADFF_{eye}': ADFF,
                                 })
        features.append({
            # 'ADB': scipy.mean(getDistances_betweenEyes(record))

            'ADB': scipy.mean(getDistances_betweenEyes(record))
        })

        if shouldAddRecord:
            featured_records.append({'Record id': record[0],
                                     'Features': features})
        features = []
    return featured_records


def features_avg_dist_figFixations(record, taskPositions, eye):
    numFixations = len(set([pos[0] for pos in taskPositions])) * \
                   len(set([pos[1] for pos in taskPositions]))
    x = record[1][f'{eye}_x'].values
    y = record[1][f'{eye}_y'].values

    fixations_ranges = []
    startFix = 0
    for i in range(1, len(taskPositions)):
        if taskPositions[i] != taskPositions[i-1]:
            fixations_ranges.append([startFix, i-1])
            startFix = i
    # appending last fixation
    fixations_ranges.append([startFix, len(taskPositions) - 1])

    average_distances = []
    for range_fix in fixations_ranges:
        fixation_distances = []
        for i in range(range_fix[0], range_fix[1] + 1):
            fixation_distances.append(distance.euclidean([x[i], y[i]], taskPositions[i]))
        average_distances.append(scipy.mean(fixation_distances))

    leftSideDistances = average_distances[0:5] + average_distances[10:15] + average_distances[20:25]
    rightSideDistances = average_distances[5:10] + average_distances[15:20] + average_distances[25:30]
    firstFixationsDistances = average_distances[0] + average_distances[10] + average_distances[20]
    return average_distances, scipy.mean(leftSideDistances), \
           scipy.mean(rightSideDistances), scipy.mean(firstFixationsDistances)




