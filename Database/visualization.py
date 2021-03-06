import matplotlib.pyplot as plt

from Clustering_Framework.clustering_parameters import *
from Database.analysis import *
from Clustering_Framework.utils import *
from Clustering_Framework.ClusteringMethods.FOSC.util.plotting import *
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from datetime import datetime
import operator

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

def get_PCA_data(X):
    pca = PCA(2)
    pca.fit(X)
    pca_data = pd.DataFrame(pca.transform(X))
    x = np.array(preprocessing.minmax_scale(pca_data[0]))
    y = np.array(preprocessing.minmax_scale(pca_data[1]))

    return x, y

def plot_pairwise_frequency_info(obj_pairwise_freq, means, rec_ids, savePlot=False):
    sorted_pairs = sorted(enumerate(means), key=operator.itemgetter(1))
    sorted_pairs_ids = [(rec_ids[pair[0]], pair[1]) for pair in sorted_pairs]
    # sorted_pairs_means = [(rec_ids[pair[0]], pair[1]) for pair in sorted_pairs]

    # sorted_pairs_
    # it doesn't need to be so rigid, could also use like the second or third best frequency...
    best_frequency = max([pair[1] for pair in sorted_pairs_ids])

    worst_records = filter(lambda x: x[1] < best_frequency, sorted_pairs_ids)
    worst_records_ids = [rec[0] for rec in worst_records]

    cmap = plt.cm.get_cmap('flare')
    rec_colors = []
    for mean in [pair[1] for pair in sorted_pairs_ids]:
        rgba = cmap(mean)
        rec_colors.append(rgba)

    print("Plotting pairwise frequency..")
    plt.figure(figsize=(30, 20))

    plt.text(500, 0.1, f'{len(worst_records_ids)} Worst Records:\n', fontsize=30, ha='right', va='top')


    for i, rec in enumerate(worst_records_ids[:120]):
        if i < 40:
            plt.text(450, 20+(i*10), rec, fontsize=30, ha='right', va='top', color=rec_colors[i])
        elif i < 80:
            plt.text(480, 20+((i-40)*10), rec, fontsize=30, ha='right', va='top', color=rec_colors[i])
        else:
            plt.text(510, 20+((i-80)*10), rec, fontsize=30, ha='right', va='top', color=rec_colors[i])

    sns.heatmap(round(pd.DataFrame(obj_pairwise_freq), 2), cmap='flare', vmin=0, vmax=1)
    plt.title(f'Pairwise Frequency of {len(rec_ids)} Recors', fontsize=80)

    if savePlot:
        plt.savefig(f'./ClusterValidation/Plots Best Clusterings/Results_{len(rec_ids)}_records/Pairwise Frequency')
        plt.close();
    plt.show()


def columnsForBothEyes(features):
    features_both_eyes = []
    for feature in features:
        if feature == 'ADB':
            features_both_eyes.append(f'{feature}')
        else:
            features_both_eyes.append(f'{feature}_left')
            features_both_eyes.append(f'{feature}_right')

    return features_both_eyes

def plot_result(result, rec_ids, savePlot=False):
    #TODO: Usar outros algoritmos para visualizar os dados em 2d:
    # - https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    # - https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html
    #Plotting Scattered data
    pca_x, pca_y = get_PCA_data(result['Data'])
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(30, 15))
    # axes[0].scatter()

    for g in np.unique(result['Partition']):
        ix = np.where(result['Partition'] == g)
        axes[0].scatter(pca_x[ix], pca_y[ix], c=plt.viridis(), label=g, s=100)
    axes[0].legend()
    axes[0].set_title(f'Method: {result["Method"]}, Parameters-> {getMethodInfo(result)}\n' 
              f'Eye: {result["Eye"]}, Features Subset: {result["Features Subset"]},\n'
              f'Silhouette: {result["Cluster Validation"]["Silhouette"]}, '
              # f'AUCC: {result["Cluster Validation"]["AUCC"]}\n'
              # f'Calinski-Harabasz Index: {result["Cluster Validation"]["Calinski-Harabasz Index"]}\n'
              # f'David-Bouldin Index": {result["Cluster Validation"]["David-Bouldin Index"]}, '
              # f'Dunn Index: {result["Cluster Validation"]["Dunn Index"]}\n'
            )
    for i in range(len(pca_x)):
        axes[0].annotate(rec_ids[i], (pca_x[i] + 0.003, pca_y[i]), fontsize=8)


    #Plotting decision tree
    labeled_data = pd.DataFrame(result['Data'], columns=result['Features Subset'])
    labeled_data['label'] = result['Partition']

    clf = DecisionTreeClassifier(random_state=1234)
    model = clf.fit(result['Data'], result['Partition'])
    sklearn.tree.plot_tree(model, feature_names=labeled_data.columns,
                           filled=True, class_names=True, ax=axes[1]);
    axes[1].set_title("Decision Tree", fontsize=40)

    if savePlot != False:
        print("Saving plot of clustering result...")
        title = f'{result["Method"]}_{result["Eye"]}_{result["Features Subset"]}_' \
                f'{datetime.now().strftime("%b-%d-%Y %Hh%Mm%Ss")} {str(datetime.now().microsecond)}ms'

        plt.savefig(f'./ClusterValidation/Plots Best Clusterings/{len(rec_ids)} recordings/{result["Method"]}/{title}')
        plt.close(fig)
        return
    plt.show()


def plotCorrelationMatrix(df):
    f = plt.figure(figsize=(19, 15))
    plt.matshow(df.corr(), fignum=f.number, cmap='flare')
    plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns,
               fontsize=14,
               rotation=45)
    plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns,
               fontsize=14)
    cb = plt.colorbar(cmap='flare')
    cb.ax.tick_params(labelsize=14)
    plt.title('Correlation Matrix', fontsize=16);
    plt.show()
    plt.close(f)

def plot_decision_tree(result):
    if result['Eye'] == 'both':
        labeled_data = pd.DataFrame(result['Data'], columns=columnsForBothEyes(result['Features Subset']))
    else:
        labeled_data = pd.DataFrame(result['Data'], columns=result['Features Subset'])
    labeled_data['label'] = result['Partition']

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=300)
    clf = DecisionTreeClassifier(random_state=1234)
    model = clf.fit(result['Data'], result['Partition'])
    sklearn.tree.plot_tree(model,
                           feature_names=labeled_data.columns,
                           filled=True,
                           class_names=True);

    plt.show()

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

    plt.title(f'Method: {result["Method"]}, Eye: {result["Eye"]}, \n'
              f'Features Subset: {result["Features Subset"]}, \n'
              f'Parameters-> {getMethodInfo(result)}\n'
              f'Silhouette: {result["Cluster Validation"]["Silhouette"]}\n'
              # f'AUCC: {result["Cluster Validation"]["AUCC"]}\n'
              # f'Calinski-Harabasz Index: {result["Cluster Validation"]["Calinski-Harabasz Index"]}\n'
              # f'David-Bouldin Index": {result["Cluster Validation"]["David-Bouldin Index"]}\n'
              # f'Dunn Index: {result["Cluster Validation"]["Dunn Index"]}\n'
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



