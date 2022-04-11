import matplotlib.pyplot as plt

from Database.analysis import *
from Clustering_Framework.utils import *

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

#Connecting to database
print("Connecting to CnLook database...")
conn = connect_db("127.0.0.1", "cnlook_")

#Reading records
groupId = "2"
taskId = "2515"
print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
records = list(getRecordings_ByTaskId(conn, groupId, taskId))
task = getTask_ById(conn, taskId)

#Closing connection to database
print("Closing connection to CnLook database...")
conn.close()


print('testing...')
for rec in records:
    plot_Record_HV(rec, task)




