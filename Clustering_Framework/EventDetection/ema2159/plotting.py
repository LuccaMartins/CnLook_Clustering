import matplotlib.pyplot as plt
import numpy as np


def plot_gaze(gaze_data):
    '''Plot the gaze data.
    Parameters:
    gaze_data: gaze data in (x_vals, y_vals) format'''
    x_data = gaze_data[0]
    y_data = gaze_data[1]
    plt.title("Gaze data", fontsize=20)
    plt.xlabel("x position", fontsize=14)
    plt.ylabel("y position", fontsize=14)
    plt.scatter(x_data, y_data, s=5, color='navy')
    plt.show()

def plot_vels(vels, sacc_thrs=None, fix_thrs=None):
    '''Plot the velocity data. Optionally plot the saccade and fixation
    thresholds.
    Parameters:
    vels: a list with the velocity data
    sacc_thrs: Velocity threshold in pixels for a point to be considered a saccade.
    fix_thrs: Velocity threshold in pixels for a point to be considered a fixation.
    '''
    plt.plot(vels, label='Velocities')
    if sacc_thrs:
        plt.hlines(sacc_thrs,
                   0,
                   len(vels),
                   colors='k',
                   linestyles='dashed',
                   label='Saccaade threshold')
    if fix_thrs:
        plt.hlines(fix_thrs,
                   0,
                   len(vels),
                   colors='k',
                   linestyles='dashdot',
                   label='Fixation threshold')
    plt.xlim(0, len(vels))
    plt.title("Velocity between points", fontsize=20)
    plt.xlabel("Point number (n)", fontsize=14)
    plt.ylabel("Point to point velocity (u/sec)", fontsize=14)
    plt.legend()
    plt.show()

def plot_simple(saccades, fixations, centroids, recording_id):
    if len(fixations) < 2 or len(saccades) < 2:
        plt.title(f"Bad event detection for record {recording_id} - ignore", fontsize=20)
        plt.show()
    else:
        flat_fix = [point for fix_group in fixations for point in fix_group]
        flat_saccade = [point for saccade_group in saccades for point in saccade_group]
        fixX, fixY = np.array(flat_fix).T
        saccX, saccY = np.array(flat_saccade).T
        centX, centY = np.array(centroids).T
        plt.title(f"Saccades, fixations and centroids\n for record {recording_id}", fontsize=20)
        plt.xlabel("x position", fontsize=14)
        plt.ylabel("y position", fontsize=14)
        plt.scatter(saccX, saccY, s=5, color="b", label="Saccades")
        plt.scatter(fixX, fixY, s=5, color="g", label="Fixations")
        plt.scatter(centX, centY, s=300, color="r", alpha=0.7, label="Centroids")
        plt.legend(borderpad=1)
        plt.axis('equal')
        plt.show()

def plot_centroids(centroids, centroids_count):
    fig, ax = plt.subplots()
    x, y = np.array(centroids).T
    # Draw fixation circles
    size = max(centroids_count)/50
    for i in range(len(centroids)):
      ax.add_artist(plt.Circle((x[i], y[i]), centroids_count[i]/size, color='r'))
    # Draw saccade lines
    for i in range(1, len(centroids)):
      plt.plot(x[i-1:i+1], y[i-1:i+1], 'b-')
    plt.title("Centroids", fontsize=20)
    plt.xlabel("x position", fontsize=14)
    plt.ylabel("y position", fontsize=14)
    plt.axis('equal')
    plt.show()