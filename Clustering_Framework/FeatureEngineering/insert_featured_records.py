from Clustering_Framework.RecordSelection.record_selection import *
from feature_engineering import *
from Database.analysis import *
from Database.inserting import *
from Clustering_Framework.utils import *

#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "cnlook_")


#Reading data
# groupId = "2" #We won't specify the group here
print('Reading task from database...')
taskId = 2515
task = getTask_ById(conn, taskId)
print(f'Reading records from database:  TaskId: {taskId}')
records = list(getRecordings_ByTaskId(conn, taskId))


print(f'Num of records: {len(records)}')
#Analyze subset of records:
good_records = analyzeRecords(records)

features = ['ADpFF-----']
#Apply feature engineering and create objects
featuredRecords = createFeaturedRecords(task, good_records, features)

insert_records(conn, featuredRecords)

print('end.........')