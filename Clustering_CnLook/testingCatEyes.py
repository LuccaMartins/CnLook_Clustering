from hvl_code.analysis import *
from utils import *

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt

from cateyes import (sfreq_to_times, classify_nslr_hmm, continuous_to_discrete,
                     plot_segmentation, plot_trajectory, classify_velocity, mad_velocity_thresh, classify_dispersion,
                     classify_remodnav)
from cateyes import sample_data_path




# # load the example data
# data_path = sample_data_path("example_data")
# data = np.genfromtxt(data_path, dtype=float, delimiter=',', names=True)
# times, x, y = data["Timestamp"], data["Theta"], data["Phi"]



#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "CnLook_DB")

#Reading records
groupId = "2"
taskId = "2515"
print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
records = list(getRecordings_ByTaskId(conn, groupId, taskId))

for record in records:
    plt.close()
    x = record[1]['left_x']
    y = record[1]['left_y']
    times = record[1]['timestamp']

    # convert the our radian data to degrees
    x_deg = np.rad2deg(x)
    y_deg = np.rad2deg(y)

    # classify the data using NSLR-HMM
    #segment_id, segment_class = classify_nslr_hmm(x_deg, y_deg, times, optimize_noise=False)

    # classify the data using I-VT
    # velocity_threshold = mad_velocity_thresh(x_deg, y_deg, times, th_0=100, return_past_threshs=False)
    # print('velocity threshold: ' + str(velocity_threshold))
    # segment_id, segment_class = classify_velocity(x_deg, y_deg, times, velocity_threshold, return_discrete=False)

    print('testes...')

    # classify the data using I-DT
    segment_id, segment_class = classify_dispersion(x_deg, y_deg, times, 0.5, 50, return_discrete=False)

    # classify the data using REMoDNaV
    # segment_id, segment_class = classify_remodnav(x_deg, y_deg, times, px2deg=1., return_discrete=False,
    #                   return_orig_output=False, simple_output=False, preproc_kwargs=dict(savgol_length=1.5))



    # convert continuous ids and descriptions to discrete timepoints and descriptions
    (seg_time, seg_class) = continuous_to_discrete(times, segment_id, segment_class)

    # plot the classification results
    fig, axes = plt.subplots(2, figsize=(15, 6), sharex=True)
    plot_segmentation(x_deg, times, segments=(seg_time, seg_class), events=None, ax=axes[0])
    plot_segmentation(y_deg, times, segments=(seg_time, seg_class), events=None, ax=axes[1], show_legend=True)

    print(f'record id: {record[0]}')
    plt.show()


    # plot trajectory
    # plot_trajectory(x_deg[:900], y_deg[:900], times[:900], segments=(seg_time, seg_class));
    #
    # plt.show()

    print('done.')

















