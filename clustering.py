from sklearn.cluster import KMeans
import pandas as pd
#import seaborn as sns; sns.set()  # for plot styling
import matplotlib.pyplot as plt


def kMeans(data, n_clusters):
    kmeans = KMeans(n_clusters)
    kmeans.fit(data)
    return kmeans.predict(data)

def printLabels(records, labels):
    i = 0

    print('')
    for label in labels:
        if label == 0:
            print('Record id:' + str(records[i].recording_id) + ', label: ' + str(label))
        i += 1

    print('cluster 1:')
    i = 0
    for label in labels:
        if label == 1:
            print('Record id:' + str(records[i].recording_id) + ', label: ' + str(label))
        i += 1
