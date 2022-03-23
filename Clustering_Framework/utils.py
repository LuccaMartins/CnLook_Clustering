from FOSC.util.fosc import FOSC

import numpy as np
from dtaidistance import dtw, dtw_ndim
from sklearn import metrics
from scipy.cluster.hierarchy import linkage, dendrogram
import json

from cateyes import (sfreq_to_times, classify_nslr_hmm, continuous_to_discrete,
                     plot_segmentation, plot_trajectory, classify_velocity, mad_velocity_thresh, classify_dispersion,
                     classify_remodnav)

import matplotlib.pyplot as plt


Dict_Groups = {
    '1': "default group",
    '2': "moivaro",
    '3': "Austevoll",
    '4': "tysnes",
    '5': "Arusha",
    '6': "moivaroIntellectuallyImpaired",
    '8': "ArushaPreTraining",
    '9': "ArushaPostTraining",
    '10': "ArushaRescreening",
    '11': "ArushaControl",
    '12': "DAT"
}


def selectFeatures(recordings, features):
    X_features = []
    for feature in features:
        X_features.append([np.array(rec[1][feature].values, dtype=np.double) for rec in recordings])
        # X_features.append(list(map(lambda x: np.array(x[1][feature].values, dtype=np.double), recordings)))

    result = []
    # for each recording
    for i in range(0, len(recordings)):
        # T.append(np.array([T_right_x[i], T_right_y[i], T_left_x, T_left_y]))
        values = []
        # for each stamp
        for j in range(0, len(recordings[i][1])):
            # values.append(np.array([T_right_x[i][j], T_right_y[i][j], T_left_x[i][j], T_left_y[i][j]]))
            valuesToAppend = []
            for feature_values in X_features:
                valuesToAppend.append(feature_values[i][j])
            values.append(np.array(valuesToAppend))
        result.append(np.array(values))
    return result

def normalizeTimestamps(timestamps):
    normalized = [0]
    for i in range(1, len(timestamps)):
        normalized.append(normalized[i-1] + timestamps.array[i]/1000 - timestamps.array[i-1]/1000)
    return normalized

def createFeaturedRecords(records):
    print('Starting feature engineering...')

    featured_records = []
    for record in records:
        segment_id, segment_class = identify_events(record, 'I-VT', savePlot="./Event Detection/Plots EventDetection")

    return featured_records

def getTaskPositions(task, timestamps):
    #TODO: this function must be different depending on the parameter_type of the task.
    # i.e., finding task position for Fixation Tasks is different from Smooth Pursuit Tasks, because
    # the positions are store differently in the database.
    normalized_Positions = json.loads(task.animation_blueprint.values[0])['NormalizedPositionDurations']

    taskPositions = []
    # for timestamp in timestamps:
    #     flag = False
    #     for position in normalized_Positions:
    #         if position['DurationSoFarInMs'] >= timestamp:
    #             x, y = position['ToPoint'].split(',')
    #             taskPositions.append([float(x), float(y)])
    #             flag = True
    #             break
    #     if flag == False:
    #         taskPositions.append([float(x), float(y)])


    # for timestamp in timestamps:
    #     for position in normalized_Positions:
    #         if position['DurationSoFarInMs'] <= timestamp:
    #             x, y = position['ToPoint'].split(',')
    #             taskPositions.append([float(x), float(y)])
    #             break


    for timestamp in timestamps:
        flag = False
        for i in range(0, len(normalized_Positions)-1):
            if normalized_Positions[i]['DurationSoFarInMs'] <= timestamp < normalized_Positions[i+1]['DurationSoFarInMs']:
                x, y = normalized_Positions[i]['ToPoint'].split(',')
                taskPositions.append([float(x), float(y)])
                flag = True
                break
        if flag == False:
            # if it wasn't in any interval of the Normalized Positions, then it belongs to the last figure position
            x, y = normalized_Positions[-1]['ToPoint'].split(',')
            taskPositions.append([float(x), float(y)])

    return taskPositions

def identify_events(record, algorithm, savePlot=None):
    #TODO: the following message appeared in one of the executions...
    # UserWarning:
    # Irregular sampling rate detected. This can lead to impaired performance with this classifier. Consider resampling your data to a fixed sampling rate. Setting sampling rate to average sample difference.
    #   warnings.warn(WARN_SFREQ)


    x = record[1]['left_x']
    y = record[1]['left_y']
    times = record[1]['timestamp']

    # convert the our radian data to degrees
    x_deg = np.rad2deg(x)
    y_deg = np.rad2deg(y)

    if algorithm == 'I-VT':
        #TODO:
        # It may not be a good idea to use different velocity thresholds for each record. I'll consider discussing
        # the best configuration with Qasim and Jadson.
        velocity_threshold = mad_velocity_thresh(x_deg, y_deg, times, th_0=100, return_past_threshs=False)
        print(f'Velocity threshold: {velocity_threshold}')
        seg_id, seg_class = classify_velocity(x_deg, y_deg, times, velocity_threshold, return_discrete=False)

    elif algorithm == "I-DT":
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
        plot_segmentation(x_deg, times, segments=(seg_time, seg_class), events=None, ax=axes[0])
        plot_segmentation(y_deg, times, segments=(seg_time, seg_class), events=None, ax=axes[1], show_legend=True)

        print(f'record id: {record[0]}')
        #plt.show()
        plt.savefig(f'{savePlot}/{algorithm}, Record {record[0]}')
        plt.close(fig)

    return seg_id, seg_class


def getSetOfSizes(recordings):
    return sorted(set([len(x) for x in recordings]))


def printBestSilhouettes(results):
    allSilhouettes_values = [col[3] for col in results]
    maxSilhouette = max(allSilhouettes_values)
    indexes = [i for i, x in enumerate(allSilhouettes_values) if x == maxSilhouette]

    for idx in indexes:
        print("Best Silhouette Validation: " + str(maxSilhouette) +
              " using minCSize = " + str(results[idx][0]) +
              ", and method = " + results[idx][1])


def analyzeRecords(records):
    # Selecting features from eye-tracker data
    features = ['tracking_status', 'left_x', 'left_y', 'right_x', 'right_y', 'left_pupil_diameter_mm', 'right_pupil_diameter_mm']
    X = selectFeatures(records, features)

    # ... here I will analyze the consistency of the records, the size difference between the timeseries, etc...


    print(f"Size difference in timestamps: ")


def generateDistanceMatrix(X, metric):
    # drop 'tracking_status'
    X = [np.array([s[1:] for s in record], dtype=np.double) for record in X]

    # get a sample to count the features (dimensions)
    n_dimensions = len(X[0][0])

    if metric == 'dtw':
        print(f"Producing distance matrix with dtw for {len(X)} series of {n_dimensions}-dimensions...")
        mat = dtw_ndim.distance_matrix_fast(X, n_dimensions)

    return mat

def startFOSC(X, savePath=None):
    # Calculating distance matrix
    mat = generateDistanceMatrix(X, 'dtw')

    listOfMClSize = [2, 4, 5, 8, 16, 20, 30]
    methodsLinkage = ["single", "average", "ward", "complete", "weighted"]
    results = []

    for m in listOfMClSize:
        print("--------------------------------------- MCLSIZE = %d ---------------------------------------" % m)

        for lm in methodsLinkage:
            print("Calling linkage with " + lm + " passing the distances matrix...")
            Z = linkage(mat, method=lm)

            foscFramework = FOSC(Z, mClSize=m)
            infiniteStability = foscFramework.propagateTree()
            partition = foscFramework.findProminentClusters(1, infiniteStability)

            # validação do algoritmo: silhouette ou AUC Under Curve
            if len(set(partition)) > 1:
                silhouette = metrics.silhouette_score(mat, partition, metric="precomputed")
                results.append([m, lm, partition, silhouette])
            else:
                results.append([m, lm, partition, -1])

            if savePath != None:
                titlePlot = f"{savePath}, mClSize: {m}\nLinkage Method: {lm}, Num of Objects: {len(X)}"
                saveDendrogram = f"./FOSC Results/Dendrogram {savePath} - mClSize {m} - {lm}.png"

                # Plot results
                plotDendrogram(Z, partition, titlePlot, saveDendrogram)
                #plotDendrogram(Z, partition, titlePlot)

    return results









#Plotting...

palleteColors = ["#80ff72", "#8af3ff", "#7ee8fa", "#89043d", "#023c40", "#c3979f", "#797270", "#c57b57", "#07004d",
                 "#0e7c7b", "#c33149", "#f49e4c", "#2e4057", "#f2d7ee", "#bfb48f", "#a5668b", "#002500", "#720e07",
                 "#f46036", "#78290f"]


def plotPartition(x, y, result, title, saveDescription=None):
    uniqueValues = np.unique(result)

    fig = plt.figure(figsize=(10, 5))

    dicColors = {}
    dicColors[0] = "#000000"

    for i in range(len(uniqueValues)):
        if uniqueValues[i] != 0:
            dicColors[uniqueValues[i]] = palleteColors[i]

    for k, v in dicColors.items():
        plt.scatter(x[result == k], y[result == k], color=v)

    plt.title(title, fontsize=15)

    if saveDescription != None:
        plt.savefig(saveDescription)
        plt.close(fig)
        return  #se for para salvar, não plota
    plt.show()

def plotDendrogram(Z, result, title, saveDescription=None):
    uniqueValues = np.unique(result)

    dicColors = {}
    dicColors[0] = "#000000"

    for i in range(len(uniqueValues)):
        if uniqueValues[i] != 0:
            dicColors[uniqueValues[i]] = palleteColors[i]

    colorsLeaf = {}
    for i in range(len(result)):
        colorsLeaf[i] = dicColors[result[i]]

    # notes:
    # * rows in Z correspond to "inverted U" links that connect clusters
    # * rows are ordered by increasing distance
    # * if the colors of the connected clusters match, use that color for link
    linkCols = {}
    for i, i12 in enumerate(Z[:, :2].astype(int)):
        c1, c2 = (linkCols[x] if x > len(Z) else colorsLeaf[x]
                  for x in i12)

        linkCols[i + 1 + len(Z)] = c1 if c1 == c2 else dicColors[0]

    fig = plt.figure(figsize=(10, 5))

    dn = dendrogram(Z=Z, color_threshold=None, leaf_font_size=5,
                    leaf_rotation=45, link_color_func=lambda x: linkCols[x])
    plt.title(title, fontsize=12)

    if saveDescription != None:
        plt.savefig(saveDescription)
        plt.close(fig)
        return

    plt.show()