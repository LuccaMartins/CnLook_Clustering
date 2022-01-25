from analysis import *
import numpy as np
import matplotlib.pyplot as plt



def plotTimeSeries(recId, feature, timeseries):

    # plt.plot(range(0, len(timeseries)), timeseries, label=feature)
    # plt.legend()
    # plt.show()

    # setting figure size to 12, 10
    plt.figure(figsize=(12, 10))

    # Labelling the axes and setting
    # a title
    plt.xlabel('Timestamp (ms)')
    plt.ylabel('Normalized Distance')
    plt.title('Recording ID: ' + str(recId) + ', Feature: ' + feature)

    # plotting the "A" column alone
    plt.plot(timeseries)
    plt.show()