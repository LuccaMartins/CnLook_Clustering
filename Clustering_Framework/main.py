from RecordSelection.record_selection import *
from FeatureEngineering.feature_engineering import *
from Database.analysis import *
from Database.reading import *
from ClusteringMethods.clustering_methods import *
from ClusteringMethods.clustering import *
from Clustering_Framework.clustering_parameters import *
from Clustering_Framework.ClusterValidation.cluster_validation import *

from utils import *

#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "cnlook_")


#Reading records
# groupId = "2"
taskId = "2515"
print(f'Reading records from database - TaskId: {taskId}')

# records = list(getRecordings_ByTaskId(conn, taskId, groupId))
featured_records = read_featuredRecords(conn, taskId)

#TODO: vary the identification method....
#for method in event_detection_methods:
allResults = []
for eye in eyes_combination:
    for subset in subsets_of_features:
        X = shapeFeaturedRecords(featured_records, subset, eye)
        results = startClusteringTests(X)
        allResults.append({
            'Parameters': {'Eye': eye,
                           'Features': subset,
                           },
            'Clustering Methods': results
        })

analyzeResults(allResults)

print(allResults)



