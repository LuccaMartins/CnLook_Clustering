from cateyes import (sfreq_to_times, classify_nslr_hmm, continuous_to_discrete,
                     plot_segmentation, plot_trajectory, classify_velocity, mad_velocity_thresh, classify_dispersion,
                     classify_remodnav)

import matplotlib.pyplot as plt
import numpy as np

from Clustering_Framework.utils import *

def identify_events(record, eye, algorithm, savePlot=None):
    #TODO: the following message appeared in one of the executions...
    # UserWarning:
    # Irregular sampling rate detected. This can lead to impaired performance with this classifier. Consider resampling your data to a fixed sampling rate. Setting sampling rate to average sample difference.
    #   warnings.warn(WARN_SFREQ)


    x = record[1][f'{eye}_x']
    y = record[1][f'{eye}_y']
    times = normalizeTimestamps(record[1]['timestamp'].array)

    # convert the our radian data to degrees
    x_deg = np.rad2deg(x)
    y_deg = np.rad2deg(y)


    if algorithm == 'I-VT':
        #TODO:
        # It may not be a good idea to use different velocity thresholds for each record. I'll consider discussing
        # the best configuration with Qasim and Jadson.
        velocity_threshold = mad_velocity_thresh(x_deg, y_deg, times, th_0=100, return_past_threshs=False)
        # print(f'Velocity threshold: {velocity_threshold}')
        seg_id, seg_class = classify_velocity(x_deg, y_deg, times, velocity_threshold, return_discrete=False)

    elif algorithm == "I-DT":
        # seg_id, seg_class = classify_dispersion(x_deg, y_deg, times, 0.5, 50, return_discrete=False)
        seg_id, seg_class = classify_dispersion(x_deg, y_deg, times, 0.5, 50, return_discrete=False)

    elif algorithm == 'REMODNAV':
        seg_id, seg_class = classify_remodnav(x_deg, y_deg, times, px2deg=1., return_discrete=False,
                          return_orig_output=False, simple_output=False, preproc_kwargs=dict(savgol_length=1.5))

    elif algorithm == 'NSLR-HMM':
        seg_id, seg_class = classify_nslr_hmm(x_deg, y_deg, times, optimize_noise=False)


    if savePlot != None:
        # convert continuous ids and descriptions to discrete timepoints and descriptions
        (seg_time, seg_class) = continuous_to_discrete(times, seg_id, seg_class)

        # plot the classification results
        fig, axes = plt.subplots(2, figsize=(15, 6), sharex=True)
        plot_segmentation(x_deg, np.array(times), segments=(seg_time, seg_class), events=None, ax=axes[0])
        plot_segmentation(y_deg, np.array(times), segments=(seg_time, seg_class), events=None, ax=axes[1], show_legend=True)

        print(f'Saving plot of EventDetection for Record id: {record[0]}, {eye} eye')
        #plt.show()
        plt.savefig(f'{savePlot}/{algorithm}, {eye}, Record {record[0]}')
        plt.close(fig)

    return seg_id, seg_class


def getMovementsInfo(record, eye, segment_id, segment_class):

    movements_ranges = getMovementsRanges(segment_id, segment_class)
    movements_positions = getMovementsPositions(record, eye, movements_ranges)

    return movements_positions

def getMovementsPositions(record, eye, movements_ranges):
    movements_positions = {}
    for type_of_movement in movements_ranges:
        movements_positions[type_of_movement] = []

    current_movement = []
    for type_of_movement in movements_ranges:
        for idxs_range in movements_ranges[type_of_movement]:
            for i in range(idxs_range[0], idxs_range[1] + 1):
                current_movement.append((record[1][f'{eye}_x'].values[i],
                                        record[1][f'{eye}_y'].values[i]))
            movements_positions[type_of_movement].append({'Range': idxs_range, 'Positions': current_movement})
            current_movement = []

    return movements_positions


def getMovementsRanges(segment_id, segment_class):

    type_of_movements = list(set(segment_class))
    movements_ranges = {}
    for type in type_of_movements:
        movements_ranges[type] = []

    movement_start = 0
    current_class_id = 0
    for i in range(1, len(segment_id)):
        if segment_id[i] != segment_id[i-1]:
            movements_ranges[segment_class[current_class_id]].append((movement_start, i-1))
            movement_start = i
            current_class_id += 1

    return movements_ranges

