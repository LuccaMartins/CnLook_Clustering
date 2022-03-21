from hvl_code.analysis import *
from utils import *


#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "CnLook_DB")


#Reading records
groupId = "2"
taskId = "2515"
print('Reading records from database: ' + Dict_Groups.get(groupId) + " - TaskId: " + taskId)
records = list(getRecordings_ByTaskId(conn, groupId, taskId))

#Analyze subset of records:
analyzeRecords(records)

#Apply feature engineering and create objects
X = createFeaturedRecords(records)

#Call clustering methods
# results = startFOSC(X, savePath=f"Task Id {taskId} ")
results = startFOSC(X)

#Analyze FOSC results
printBestSilhouettes(results)




