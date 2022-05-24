from Clustering_Framework.RecordSelection.record_selection import *
from feature_engineering import *
from Database.analysis import *
from Database.inserting import *
from Clustering_Framework.utils import *
from Database.visualization import *

#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "cnlook_")


#Reading data
print('Reading task from database...')
#TODO: Use the specific task for each record (not essential, tasks have the same animation_blueprint)
taskId = 2515
task = getTask_ById(conn, taskId)
print(f'Reading records from database (all tasks similar to Task {taskId})')
records = list(getRecordings_SameTasks(conn).groupby(['recording_id']))

# plot_Record_HV(records[0], task)

print(f'Num of records: {len(records)}')
#Analyze subset of records:
# good_records = analyzeRecords(records)
good_records = records

#Apply feature engineering and create objects
featuredRecords = createFeaturedRecords(task, good_records)

insert_featuredRecords(conn, featuredRecords)

print('end.........')