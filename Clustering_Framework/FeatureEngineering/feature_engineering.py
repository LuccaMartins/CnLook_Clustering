from Clustering_Framework.EventDetection.event_Detection import *
from Clustering_Framework.utils import *

from scipy.spatial import distance
import pandas as pd

class Fixation:
  def __init__(self, idx_begin, idx_end, positions):
    self.begin = idx_begin
    self.end = idx_end
    self.positions = positions

  def myfunc(self):
    print("Hello my name is " + self.name)


def createFeaturedRecords(task, records):
#ToDo: from https://doi.org/10.3390/app11136157  (Sáiz-Manzanares, 2021)
# FC - Fixation Count
# AFD - Average duration of fixation
# FDMax - Maximum duration of fixation
# FDMin - Minimum duration of fixation
# Sum of all dispersions of fixations in X and Y
# FDT - Fixation Total Dispersion
# FDA - Fixation Dispersion Average
# ---
# SC - Saccade Count
# SFC - Sum of all saccades
# SDT - Sum of the duration of all saccades
# SDMax - Maximum saccade duration
# SDMin - Minimum saccade duration
# SAT - Sum of the amplitude of all saccades
# SAMax - Maximum of saccade amplitude
# SAMin - Minimum of saccade amplitude
#
    print('Starting feature engineering...')
    featured_records = []

    for eye in 'left', 'right':
        for record in records:
            segment_id, segment_class = identify_events(record, eye, 'I-VT',
                                                        savePlot="./EventDetection/Plots EventDetection")
            movements = getMovementsInfo(record, eye, segment_id, segment_class)

            # records have different sizes...
            taskPositions = getTaskPositions(task, normalizeTimestamps(record[1]['timestamp'].array))

            # distancesToTarget = getFixationsDistances_ToTarget(taskPositions, fixations_positions)

            # FC - Fixation Count
            count_fixations = len(movements['Fixation'])
            # SC - Saccade Count
            count_saccades = len(movements['Saccade'])

            featured_records.append([record[0], count_fixations, count_saccades])



    return featured_records


def getFixationsDistances_ToTarget(taskPositions, fixations):
    allDistances = []

    distances = []

    for fixation in fixations:
        i = fixation[0][0]
        for pos in fixation[1]:
            distanceToTarget = distance.euclidean(pos, taskPositions[i])
            i += 1




