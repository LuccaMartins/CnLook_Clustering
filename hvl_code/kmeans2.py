from sklearn.cluster import KMeans
from analysis import *
import numpy as np
import matplotlib.pyplot as plt
import collections, numpy
import psycopg2
import pandas as pd
import scipy.interpolate
import scipy.stats
import scipy.signal
import ast
import sklearn.decomposition
from sklearn.base import BaseEstimator, TransformerMixin
import matplotlib.pyplot as plt
import re
from pandas import DataFrame
from matplotlib.pyplot import figure

conn = connect_db("127.0.0.1","candlook_hvl")


df = read_task_data(conn, "moivaroIntellectuallyImpaired", "DiagonalRightAndBack")

recordsByTask = list(df.groupby(df.index))
recordsByTask

X = []
for record in recordsByTask:
    X.append(list(record[1].left_x))



kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

y_kmeans