from Clustering_Framework.RecordSelection.record_selection import *
from feature_engineering import *
from Database.analysis import *
from Database.inserting import *
from Clustering_Framework.utils import *
from Database.visualization import *

conn = connect_db("127.0.0.1", "cnlook_")

# Reading data
print('Reading task 2515 from database...')

# We can use only task 2515 for every record from other similar tasks, because all similar tasks
# have the same animation_blueprint.
taskId = 2515
task = getTask_ById(conn, taskId)

print(f'Reading records from database (all similar to Task {taskId})')
records = list(getRecordings_SimilarTasks(conn, taskId).groupby(['recording_id']))

print(f'Num of records: {len(records)}')
#Analyze subset of records:

good_records = analyzeRecords(records)
good_records = records

#Apply feature engineering and create objects
featuredRecords = createFeaturedRecords(task, good_records)

insert_featuredRecords(conn, featuredRecords)

print('end.........')