from cateyes import (sfreq_to_times, classify_nslr_hmm, continuous_to_discrete,
                     plot_segmentation, plot_trajectory, classify_velocity, mad_velocity_thresh, classify_dispersion,
                     classify_remodnav)
from Clustering_Framework.EventDetection.ema2159.i_vt import *
from Clustering_Framework.EventDetection.ema2159.utils import *
from Clustering_Framework.EventDetection.ema2159.plotting import *
import matplotlib.pyplot as plt
import numpy as np

from Clustering_Framework.utils import *


#

def identify_events_ema(record, eye, last_valid_idx, algorithm='IVT'):
    points = []
    points.append(list(record[1][f'{eye}_x'][:last_valid_idx]))
    points.append([1 - pos for pos in list(record[1][f'{eye}_y'])][:last_valid_idx])
    # (saccades, fixations, centroids, centroids_count) = I_VT_alg(points, 11000, 750, 100, 200)

    # (saccades, fixations, centroids, centroids_count, fixations_ranges) = I_VT_alg(points, 11000, 750, 100, 200)
    (saccades, fixations, centroids, centroids_count, fixations_ranges) = I_VT_alg(points, 11000, 4000, 200, 300, False)
    # plot_simple(saccades, fixations, centroids, record[0])
    plot_simple(saccades, fixations, centroids, record[0], savePlot=f'C:\Git Repositories\CnLook_Clustering\Clustering_Framework\EventDetection\Plots EventDetection/Record {record[0]}, EMA_{algorithm}, {eye} eye')

    return saccades, fixations, centroids, centroids_count, fixations_ranges


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

