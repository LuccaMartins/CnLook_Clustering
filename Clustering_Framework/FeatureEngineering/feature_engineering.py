from Clustering_Framework.EventDetection.event_Detection import *
from Clustering_Framework.utils import *

from scipy.spatial import distance
import pandas as pd
import scipy


all_features = [  # Check document 'Features to Extract.xlsx' in './FeatureEngineering' for explanation
    #from Fixations
    'FC', 'AFD', 'FDMax', 'FDMin', 'FDT', 'FDA',
    #from Saccades
    'SC', 'ASC',
    'SFC', 'SDMa', 'SDMi', 'SDT', 'SDA', 'SAT', 'ASA', 'SAMa', 'SAMi', 'SSV', 'SVMax', 'SVMin', 'ASL',
    #from Blinks
    'BC' , 'BFC', 'BDT', 'BDA', 'BDMax', 'BDMin',
    #Others
    'SPL', 'ADT', 'ADpFF'
]

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
    for i in range(1, len(record[1])):
        path_length += distance.euclidean([x[i-1],y[i-1]], [x[i],y[i]])

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
    #TODO: check this dispersion calculating method...
    # Here I'm simply getting the average of the dispersion of X and Y
    movements_positions = [movements[i]['Positions'] for i in range(0, len(movements))]
    dispersions = []
    total_disp_x = 0
    total_disp_y = 0
    for movement in movements_positions:
        x_values = [pos[0] for pos in movement]
        y_values = [pos[1] for pos in movement]
        disp_x = max(x_values) - min(x_values)
        disp_y = max(y_values) - min(y_values)
        dispersions.append({'disp_x': disp_x,
                            'disp_y': disp_y})
        total_disp_x += disp_x
        total_disp_y += disp_y

    total_disp = scipy.mean([total_disp_x, total_disp_y])
    average_disp = total_disp/len(movements_positions)
    return total_disp, average_disp

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
            distancesToTarget = getDistances_ToTarget(record, taskPositions, eye)
            (saccades, fixations, centroids, centroids_count, fixations_ranges) = identify_events_ema(record, eye)

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


                ADTF = scipy.mean([scipy.mean(distancesToTarget[fix[0]:fix[1]+1]) for fix in valid_fixations_ranges])
                if not ADTF:
                    print('opa')
                features.append({
                                 f'FC_{eye}': len(fixations),
                                 f'ADTF_{eye}': ADTF,
                                 f'AFD_{eye}': scipy.mean([len(x) for x in fixations]),
                                 f'FDMax_{eye}': max([len(x) for x in fixations]),
                                 f'FDMin_{eye}': min([len(x) for x in fixations]),
                                 f'FDA_{eye}': scipy.mean([np.std(fixation) for fixation in fixations]),
                                 f'SC_{eye}': len(saccades),
                                 f'ASD_{eye}': scipy.mean([len(x) for x in saccades]),
                                 f'SDMax_{eye}': max([len(x) for x in saccades]),
                                 f'SDMin_{eye}': min([len(x) for x in saccades]),
                                 f'SDA_{eye}': scipy.mean([np.std(saccade) for saccade in saccades]),
                                 f'SPL_{eye}': features_path_length(record, eye),
                                 f'ASA_{eye}': scipy.mean([distance.euclidean(saccade[0], saccade[-1]) for saccade in saccades]),
                                 f'SAMax_{eye}': max([distance.euclidean(saccade[0], saccade[-1]) for saccade in saccades]),
                                 f'SAMin_{eye}': min([distance.euclidean(saccade[0], saccade[-1]) for saccade in saccades]),
                                 f'ADT_{eye}': scipy.mean(distancesToTarget),
                                 f'ADpFF_{eye}': features_avg_dist_figFixations(record, taskPositions, eye),
                                 })

        if shouldAddRecord:
            featured_records.append({'Record id': record[0],
                                     'Features': features})
        features = []


    return featured_records

def features_task_with_fixations(task, records):
    features = []
    featured_records = []
    for record in records:
        print(f'\n-----> Extracting features from record {record[0]}')
        # records have different sizes...
        taskPositions = getTaskPositions(task, normalizeTimestamps(record[1]['timestamp'].array))
        shouldAddRecord = True
        for eye in 'left', 'right':
            distancesToTarget = getDistances_ToTarget(record, taskPositions, eye)
            segment_id, segment_class = identify_events_catEyes(record, eye, 'I-DT', savePlot="./EventDetection/Plots EventDetection")
            movements = getMovementsInfo(record, eye, segment_id, segment_class)

            if len(movements['Fixation']) > 1 and len(movements['Saccade']) > 1 and shouldAddRecord:
                shouldAddRecord = True #flag used to check quality of movement identification on both eyes
                average_fix_dur, max_fix_dur, min_fix_dur = features_event_duration(movements['Fixation'])
                average_sac_dur, max_sac_dur, min_sac_dur = features_event_duration(movements['Saccade'])

                # TODO: not sure about dispersion...
                # FDT, FDA
                # total_fix_disp, average_fix_disp = features_event_dispersion(movements['Fixation'])
                # SDT, SDA
                # total_sac_disp, average_sac_disp = features_event_dispersion(movements['Saccade'])

                # TODO: some issues with these ones.. because they need the previous and next movements positions too...
                # # SAT, ASA, SAMax, SAMin
                # sum_sac_amp, average_sac_amp, max_sac_amp, min_sac_amp = features_event_amplitude(movements['Saccades'], movements['Fixations'])
                # # SSV, SVMax, SVMin
                # sum_sac_vel, max_sac_vel, min_sac_vel = features_event_velocity(movements['Saccade'])

                features.append({
                                 f'SPL_{eye}': features_path_length(record, eye),
                                 f'FC_{eye}': len(movements['Fixation']),
                                 f'AFD_{eye}': average_fix_dur,
                                 f'FDMax_{eye}': max_fix_dur,
                                 f'FDMin_{eye}': min_fix_dur,
                                 # f'FDT_{eye}': total_fix_disp,
                                 # f'FDA_{eye}': average_fix_disp,
                                 f'SC_{eye}': len(movements['Saccade']),
                                 f'ASD_{eye}': average_sac_dur,
                                 f'SDMax_{eye}': max_sac_dur,
                                 f'SDMin_{eye}': min_sac_dur,
                                 # f'SDT_{eye}': total_sac_disp,
                                 # f'SDA_{eye}': average_sac_disp,
                                 f'ASL_{eye}': features_event_latency(movements['Saccade']),
                                 f'ADT_{eye}': scipy.mean(distancesToTarget),
                                 f'ADpFF_{eye}': features_avg_dist_figFixations(record, taskPositions, eye),
                                 })
            else:
                print('Empty list of movements for this record...')
                shouldAddRecord = False
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
    #appending last fixation
    fixations_ranges.append([startFix, len(taskPositions) - 1])

    average_distances = []
    for range_fix in fixations_ranges:
        fixation_distances = []
        for i in range(range_fix[0], range_fix[1] + 1):
            fixation_distances.append(distance.euclidean([x[i], y[i]], taskPositions[i]))
        average_distances.append(scipy.mean(fixation_distances))

    return average_distances



