import matplotlib as plt

from Database.analysis import *
from Clustering_Framework.utils import *

def plot_Record_HV(record, plotTask=False):
    record[1]['timestamp'] = normalizeTimestamps(record[1]['timestamp'])

    fig, axs = plt.subplots(2, 2, figsize=(16, 8))
    fig.canvas.manager.set_window_title(f'Record ID: {record[0]}')
    fig.suptitle('Horizontal and Vertical Gazes')
    axs[0, 0].plot(record[1]['timestamp'].array, record[1]['left_x'], color='blue')
    axs[0, 0].set_title('Horizontal Left')
    axs[0, 1].plot(record[1]['timestamp'].array, record[1]['right_x'], color='red')
    axs[0, 1].set_title('Horizontal Right')
    axs[1, 0].plot(record[1]['timestamp'].array, record[1]['left_y'], color='blue')
    axs[1, 0].set_title('Vertical Left')
    axs[1, 1].plot(record[1]['timestamp'].array, record[1]['right_y'], color='red')
    axs[1, 1].set_title('Vertical Right')

    for ax in axs.flat:
        ax.set(xlabel='ms', ylabel='%')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()


    if plotTask == True:
        # Connecting to database
        print("Connecting to CnLook Database...")
        conn = connect_db("127.0.0.1", "CnLook_DB")

        task = getTask_ByRecordingId(conn, record[0])
        taskPositions = getTaskPositions(task, record[1]['timestamp'].array)

        axs[0, 0].plot(record[1]['timestamp'].array, [pos[0] for pos in taskPositions], color='#09f919', linewidth=4, zorder=0)
        axs[0, 1].plot(record[1]['timestamp'].array, [pos[0] for pos in taskPositions], color='#09f919', linewidth=4, zorder=0)
        axs[1, 0].plot(record[1]['timestamp'].array, [pos[1] for pos in taskPositions], color='#09f919', linewidth=4, zorder=0)
        axs[1, 1].plot(record[1]['timestamp'].array, [pos[1] for pos in taskPositions], color='#09f919', linewidth=4, zorder=0)

        print(task)


    plt.show()

#Connecting to database
print("Connecting to CnLook database...")
conn = connect_db("127.0.0.1", "CnLook_DB")

#Reading records
groupId = "2"
taskId = "2511"
print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
records = list(getRecordings_ByTaskId(conn, groupId, taskId))

#Closing connection to database
print("Closing connection to CnLook database...")
conn.close()


print('testing...')
for i in range(10, 20):
    plot_Record_HV(records[i], plotTask=True)




