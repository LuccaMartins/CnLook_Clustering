from math import sqrt
from Clustering_Framework.EventDetection.ema2159.utils import *
import numpy as np


def get_vels(points, sample_rate):
    '''Function for geting the velocities between the points in a list of gaze data.
    Parameters:
    points: Eye tracking data points in the form of (x_values, y_values).
    sample_rate: Sample rate in which the gaze data was recorded.'''
    velocities = []  # List to store velocities
    x_data = points[0]
    y_data = points[1]
    # Calculate velocities between all the points
    for i in range(len(x_data) - 1):
        # Velocity (sqrt((x2-x1)^2+(y2-y1)^2)/time), with 1/time = sample rate
        velocities.append(
            sqrt(((x_data[i + 1] - x_data[i]) ** 2 + (y_data[i + 1] - y_data[i]) ** 2))
            * sample_rate
        )
    return velocities


def I_VT_alg(points, sample_rate, up_sacc_thrs, sacc_thrs, fix_thrs, filt=True):
    '''Implementation of the Velocity-Threshold Identification (I-VT) algorithm.
    Parameters:
    points: Eye tracking data points in the form of (x_values, y_values).
    sample_rate: Sample rate for calculating the velocities.
    sacc_thrs: Velocity threshold in pixels for a point to be considered a saccade.
    fix_thrs: Velocity threshold in pixels for a point to be considered a fixation.
    filt: When true, the velocity data is passed through a low pass filter

    Returns:
    saccades: A list with the points corresponding to saccades.
    fixations: A list with the groups of points corresponding to fixation groups.
    centroids: A list with the centroids of each fixation group.
    centroids_count: A list with the number of points correspondent to each centroid.
    '''
    saccades = []  # List to store saccades
    fixations = []  # List to store fixations
    fix_group = []  # Buffer list to store fixation groups
    fixations_ranges = []
    saccade_group = []  # Buffer list to store saccade groups
    x_data = points[0]
    y_data = points[1]
    vels = get_vels(points, sample_rate)
    fix_start = -1

    if filt:
        vels = butter_lowpass_filter(vels)
    # Saccades and fixations calculation
    for i in range(len(vels)):
        # If velocity over saccade threshold, add point to saccades
        if (vels[i] >= sacc_thrs and vels[i] <= up_sacc_thrs):
            # If saccade detected and fix_group buffer contains points, add the
            # group in the buffer to fixations and clear buffer
            if fix_group:
                fixations.append(fix_group.copy())
                fixations_ranges.append([fix_start, i-1])
                fix_group.clear()
            saccade_group.append([x_data[i], y_data[i]])
        # If velocity below fixation threshold, add point to fixations
        elif vels[i] <= fix_thrs:
            # If fixation detected and saccade_group buffer contains points, add the
            # group in the buffer to saccades and clear buffer
            if saccade_group:
                fix_start = i
                saccades.append(saccade_group.copy())
                saccade_group.clear()
            if fix_start == -1:
                fix_start = i
            fix_group.append([x_data[i], y_data[i]])
    # If fix_group or saccade_group buffers are not empty after
    # transversing all the points,add group in buffer to fixations
    if fix_group:
        fixations.append(fix_group)
        fixations_ranges.append([fix_start, i])
    if saccade_group:
        saccades.append(saccade_group)
    # Centroids calculation
    centroids = []
    centroids_count = []
    # For all fixation groups, calculate the middle point
    for group in fixations:
        group = np.array(group)
        group = group.T
        centroids.append([group[0].mean(), group[1].mean()])
        centroids_count.append(len(group[0]))
    return (saccades, fixations, centroids, centroids_count, fixations_ranges)