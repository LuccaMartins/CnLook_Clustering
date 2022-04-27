from math import sqrt
from Clustering_Framework.EventDetection.ema2159.utils import *
import numpy as np

def get_dists(points):
    '''Function for geting the distances between the points in a list of gaze data.
    Parameters:
    points: Eye tracking data points in the form of (x_values, y_values).
    sample_rate: Sample rate in which the gaze data was recorded.'''
    distances = []
    x_data = points[0]
    y_data = points[1]
    for i in range(len(x_data) - 1):
        distances.append(
            sqrt(((x_data[i + 1] - x_data[i]) ** 2 + (y_data[i + 1] - y_data[i]) ** 2))
        )
    return distances

def I_DT_alg(points, disp_thrs, min_count):
    saccades = [[]]
    fixations = []
    centroids = []
    centroids_count = []
    x_data, y_data, = points
    dists = get_dists(points)
    count = 0
    i = 0
    while i < len(dists):
      current = dists[i:i+min_count]
      if len(current) < min_count or sum(current) > disp_thrs:
        saccades[-1].append([x_data[i], y_data[i]])
        i += 1
      else:
        missing = dists[i+min_count:]
        for j in range(len(missing)):
          if (sum(current) + sum(missing[:j+1])) > disp_thrs:
            break
        x, y = x_data[i:i+min_count+j], y_data[i:i+min_count+j]
        fixations.append(np.array([x,y]).T.tolist())
        centroids.append([np.mean(x), np.mean(y)])
        centroids_count.append(len(x))
        if len(saccades[-1]):
          saccades.append([])
        i += min_count + j
    fixations = np.array(fixations).T
    return (saccades, fixations, centroids, centroids_count)