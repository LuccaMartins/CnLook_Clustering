import matplotlib.pyplot as plt

from Clustering_Framework.clustering_parameters import *
from Database.analysis import *
from Clustering_Framework.utils import *
from Clustering_Framework.ClusteringMethods.FOSC.util.plotting import *
from sklearn.decomposition import PCA
import seaborn as sns


from matplotlib import colors as mcolors
import math

from mpl_toolkits.mplot3d import Axes3D

def scatter_indic(data):
    #alternatively you can calulate any other indicators
    max = np.max(data, axis=1)
    min = np.min(data, axis=1)
    return max, min

def getMethodInfo(result):
    method = result['Method']
    methodInfo = result['Method Info']
    if method == 'FOSC':
        string = f"MinClusterSize: {methodInfo['MinClusterSize']}, " \
                 f"'Linkage Method: {methodInfo['Linkage Method']}"
    elif method == 'DBSCAN':
        string = f"Eps: {methodInfo['Eps']}, " \
                 f"Min Samples: {methodInfo['Min Samples']}"
    elif method == 'K-Means':
        string = f"K: {methodInfo['K']}"

    return string


def plot_scattered_data_PCA(X, rec_ids, result=None, savePlot=False, resultIdx=None):
    pca = PCA(2)
    pca.fit(X)
    pca_data = pd.DataFrame(pca.transform(X))
    x = np.array(pca_data[0])
    y = np.array(pca_data[1])

    if result is None:
        plt.scatter(pca_data[0], pca_data[1])
    else:
        fig, ax = plt.subplots(figsize=(15, 15))
        for g in np.unique(result['Partition']):
            ix = np.where(result['Partition'] == g)
            ax.scatter(x[ix], y[ix], c=plt.viridis(), label=g, s=100)
    ax.legend()

    plt.title(f'Method: {result["Method"]}, Eye: {result["Eye"]}, Features Subset: {result["Features Subset"]}, '
              f'Parameters-> {getMethodInfo(result)}\n'
              f'Silhouette: {result["Cluster Validation"]["Silhouette"]}\n'
              # f'AUCC: {result["Cluster Validation"]["AUCC"]}\n'
              f'Calinski-Harabasz Index: {result["Cluster Validation"]["Calinski-Harabasz Index"]}\n'
              f'David-Bouldin Index": {result["Cluster Validation"]["David-Bouldin Index"]}\n'
              f'Dunn Index: {result["Cluster Validation"]["Dunn Index"]}\n'
              )
    for i in range(len(x)):
        plt.annotate(rec_ids[i], (x[i] + 0.003, y[i]), fontsize=8)

    if savePlot:
        print('Saving Scattered Plot...')
        title = f'{result["Method"]}_{result["Eye"]}_{result["Features Subset"]}_idx {resultIdx}'
        plt.savefig(f'./ClusterValidation/Plots Best Clusterings/{title}')
        plt.close(fig)

        # if result["Method"] == 'FOSC':
        #     title = f'Dendrogram_{result["Eye"]}_{result["Features Subset"]}_idx {resultIdx}'
        #     plotDendrogram(result['Method Info']['Hierarchy'], result['Partition'], title, saveDescription='./ClusterValidation/'
        #                                                                             'Plots Best Clusterings/'
        #                                                                             'FOSC Dendrograms/')
    else:
        plt.show()

    plt.show()





def plot_Record_HV(record, task):
    timestamps = normalizeTimestamps(record[1]['timestamp'].array)

    fig, axs = plt.subplots(2, 1, figsize=(16, 8))
    fig.suptitle(f'Horizontal and Vertical Gazes for Record: {record[0]}')
    axs[0].set_title('Horizontal Left/Right')
    axs[0].plot(timestamps, record[1]['left_x'], linewidth=1, color='blue')
    axs[0].plot(timestamps, record[1]['right_x'], linewidth=1, color='red')
    axs[1].set_title('Vertical Left/Right')
    axs[1].plot(timestamps, [1 - y_pos for y_pos in record[1]['left_y']], linewidth=1, color='blue') #inverting y values
    axs[1].plot(timestamps, [1 - y_pos for y_pos in record[1]['right_y']], linewidth=1, color='red') #inverting y values

    for ax in axs.flat:
        ax.set(xlabel='ms', ylabel='%')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()


    if type(task) is pd.DataFrame:
        # Connecting to database
        # print("Connecting to CnLook Database...")
        # conn = connect_db("127.0.0.1", "cnlook_")


        taskPositions = getTaskPositions(task, timestamps)

        # axs[0].plot(timestamps[0:len(taskPositions)], [pos[0] for pos in taskPositions], color='#09f919', linewidth=7, zorder=0, linestyle='None', markersize=10.0)
        axs[0].plot(timestamps[0:len(taskPositions)], [pos[0] for pos in taskPositions], color='#09f919', zorder=0, linestyle='None', marker='|', ms=10)
        axs[1].plot(timestamps[0:len(taskPositions)], [1 - pos[1] for pos in taskPositions], color='#09f919', zorder=0, linestyle='None', marker='|', ms=10) #inverting y values
        # axs[1, 0].plot(timestamps[0:len(taskPositions)], [pos[1] for pos in taskPositions], color='#09f919', linewidth=4, zorder=0)
        # axs[1, 1].plot(timestamps[0:len(taskPositions)], [pos[1] for pos in taskPositions], color='#09f919', linewidth=4, zorder=0)

        # print(task)


    plt.show()

# #Connecting to database
# print("Connecting to CnLook database...")
# conn = connect_db("127.0.0.1", "cnlook_")
#
# #Reading records
# groupId = "2"
# taskId = "2515"
# print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
# records = list(getRecordings_ByTaskId(conn, groupId, taskId))
# task = getTask_ById(conn, taskId)
#
# #Closing connection to database
# print("Closing connection to CnLook database...")
# conn.close()
#
#
# print('testing...')
# for rec in records:
#     plot_Record_HV(rec, task)
#



