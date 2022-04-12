from Clustering_Framework.EventDetection.event_Detection import *
from Clustering_Framework.utils import *

from scipy.spatial import distance
import pandas as pd
import scipy

class Fixation:
  def __init__(self, idx_begin, idx_end, positions):
    self.begin = idx_begin
    self.end = idx_end
    self.positions = positions

  def myfunc(self):
    print("Hello my name is " + self.name)


def createFeaturedRecords(task, records):
#ToDo: from https://doi.org/10.3390/app11136157  (Sáiz-Manzanares, 2021)
# A detail here is that this paper use records of users analyzing images, instead of executing visual tasks as in our case...
# FC - Fixation Count
# AFD - Average duration of fixation
# FDMax - Maximum duration of fixation
# FDMin - Minimum duration of fixation
# FDT - Fixation Total Dispersion (Sum of all dispersions of fixations in X and Y)
# FDA - Fixation Dispersion Average
# ---
# SC - Saccade Count
# ASC - Average duration of saccade
# SFC - Sum of all saccades
# SDT - Sum of the duration of all saccades
# SDMax - Maximum saccade duration
# SDMin - Minimum saccade duration
# SAT - Sum of the amplitude of all saccades
# ASA - Average saccade amplitude
# SAMax - Maximum of saccade amplitude
# SAMin - Minimum of saccade amplitude
# SSV - Sum of the velocity of all saccades
# SVMa - Maximum saccade velocity
# SVMi - Minimum saccade velocity
# ASL - Saccade Latency Average
# ---
# BC - Bling count
# BFC - Blink frequency count
# BDT - Blink duration total
# BDA - Blink duration average
# BDMa - Maximum blink duration
# BDMi - Minimum blink duration
# ---
# SPL - Scan Path Length

    print('Starting feature engineering...')
    features = []
    featured_records = []
    for record in records:
        for eye in 'left', 'right':
            segment_id, segment_class = identify_events(record, eye, 'I-VT',
                                                        savePlot="./EventDetection/Plots EventDetection")
            movements = getMovementsInfo(record, eye, segment_id, segment_class)

            # records have different sizes...
            taskPositions = getTaskPositions(task, normalizeTimestamps(record[1]['timestamp'].array))

            distancesToTarget = getDistances_ToTarget(record, taskPositions, eye)

            # FC
            fixations_count = len(movements['Fixation'])
            # AFD, FDMa, FDMi
            average_fix_dur, max_fix_dur, min_fix_dur = features_event_duration(movements['Fixation'])
            # FDT, FDA
            total_fix_disp, average_fix_disp = features_event_dispersion(movements['Fixation'])


            # SC
            saccades_count = len(movements['Saccade'])
            # ASD, SDMa, SDMi
            average_sac_dur, max_sac_dur, min_sac_dur = features_event_duration(movements['Saccade'])
            # SDT, SDA
            total_sac_disp, average_sac_disp = features_event_dispersion(movements['Saccade'])
            # ASL
            average_sac_lat = features_event_latency(movements['Saccade'])

            #TODO: some issues with this one.. it needs the previous and next movements positions too...
            # # SAT, ASA, SAMa, SAMi
            # sum_sac_amp, average_sac_amp, max_sac_amp, min_sac_amp = features_event_amplitude(movements['Saccades'], movements['Fixations'])
            # # SSV, SVMa, SVMi
            # sum_sac_vel, max_sac_vel, min_sac_vel = features_event_velocity(movements['Saccade'])



            features.append({f'FC_{eye}': fixations_count,
                             f'AFD_{eye}': average_fix_dur,
                             f'FDMa_{eye}': max_fix_dur,
                             f'FDMi_{eye}': min_fix_dur,
                             f'FDT_{eye}': total_fix_disp,
                             f'FDA_{eye}': average_fix_disp,
                             f'SC_{eye}': saccades_count,
                             f'ASD_{eye}': average_sac_dur,
                             f'SDMa_{eye}': max_sac_dur,
                             f'SDMi_{eye}': min_sac_dur,
                             f'SDT_{eye}': total_sac_disp,
                             f'SDA_{eye}': average_sac_disp,
                             f'ASL_{eye}': average_sac_lat})

        featured_records.append({'Record id': record[0],
                                 'Features': features})
        features = []

    return featured_records

def features_event_latency(movements):
    latencies = []
    event_beginnings = [range[0] for range in [movement['Range'] for movement in movements]]
    event_endings = [range[1] for range in [movement['Range'] for movement in movements]]

    for i in range(1, len(event_beginnings)):
        latencies.append(event_beginnings[i] - event_endings[i-1] - 1)

    return scipy.mean(latencies)

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

        return average, max(durations), min(durations)

def getDistances_ToTarget(record, taskPositions, eye):

    for figurePos in taskPositions:
        print('a')




