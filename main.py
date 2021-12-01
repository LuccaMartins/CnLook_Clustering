import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import math


import database
import json
import plotter
import utils
import clustering
from hvl_code.analysis import *


conn = database.connect()
#
# recordId_1 = '946'
# recordId_2 = '5304'
#
#
# objRecord_1 = database.getRecordById(recordId_1)
# [leftPos_1, rightPos_1] = objRecord_1.getEyesPositions_HV()
# # print(leftPos, rightPos)
# plotter.positions_HV(objRecord_1)
#
# objRecord_2 = database.getRecordById(recordId_2)
# [leftPos_2, rightPos_2] = objRecord_2.getEyesPositions_HV()
# # print(leftPos, rightPos)
# X_rightPos_1 = list(map(lambda x: float(x[0]), rightPos_1))
# X_rightPos_2 = list(map(lambda x: float(x[0]), rightPos_2))
#
# plotter.positions_HV(objRecord_2)



# tList = utils.normalizeLength([X_rightPos_1, X_rightPos_2])

# print(utils.euclid_dist(np.array(tList[0]),np.array(tList[1])))








#CLUSTERING WITH KMEANS

records = database.getRecordsByTaskId('701')
records_pos = []
#
# plotter.positions_HV(records[0])
#
print('getting eyes positions...')
for rec in records:
    records_pos.append(rec.getEyesPositions_HV())

records_pos_right_X = []
print('getting right eye X positions...')
for rec_pos in records_pos:                                         #taking only right eye's positions
    records_pos_right_X.append(list(map(lambda x: float(x[0]), rec_pos[1])))

records_pos_right_X = utils.normalizeLength(records_pos_right_X)

y_kmeans = clustering.kMeans(records_pos_right_X, n_clusters=2)


clustering.printLabels(records, y_kmeans)




read_task_data(conn, "Arusha", "Animation - Task Type: Saccade Speed Test")