from RecordSelection.record_selection import *
from FeatureEngineering.feature_engineering import *
from Database.analysis import *
from ClusteringMethods.clustering_methods import *
from utils import *

#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "cnlook_")


#Reading records
groupId = "2"
taskId = "2515"
print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
records = list(getRecordings_ByTaskId(conn, groupId, taskId))
print('Reading task...')
task = getTask_ById(conn, 2515)

print(f'Num of records: {len(records)}')
#Analyze subset of records:
Y = analyzeRecords(records)



#Apply feature engineering and create objects
featuredRecords = createFeaturedRecords(task, records)

X = shapeFeaturedRecords(featuredRecords)

#Call clustering methods
# results = startFOSC(X, savePath=f"Task Id {taskId} ")
results = startFOSC(X)

#Analyze FOSC results
#printBestSilhouettes(results)




