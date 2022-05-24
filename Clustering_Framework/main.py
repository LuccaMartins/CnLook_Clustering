from RecordSelection.record_selection import *
from FeatureEngineering.feature_engineering import *
from Database.analysis import *
from Database.reading import *
from Database.inserting import *
from Database.visualization import *
from ClusteringMethods.clustering_methods import *
from ClusteringMethods.clustering import *
from Clustering_Framework.clustering_parameters import *
from Clustering_Framework.ClusterValidation.cluster_validation import *
from utils import *

from sklearn import preprocessing

#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "cnlook_")


#Reading records
# groupId = "2"
taskId = "2515"

# tasks = getTasks(conn)
# jsonsss = []
# for param_data in list(tasks['animation_blueprint']):
#     jsonsss.append(json.loads(param_data))
#
# df2 = pd.DataFrame(jsonsss)


print(f'Reading records from database ')

# records = list(getRecordings_ByTaskId(conn, taskId, groupId))
featured_records = read_featuredRecords(conn)

#TODO: vary the identification method....
#for method in event_detection_methods:
allResults = []
for eye in eyes_combination:
    for subset in subsets_of_features:
        X = shapeFeaturedRecords(featured_records, subsets_of_features.get(subset), eye)

        results = startClusteringTests(X)
        for result in results:
            result['Eye'] = eye
            result['Features Subset'] = subset
            allResults.append(result)

        # for result in results[0]['Results']:
        #     plot_scattered_data(X,
        #                         config={'Eye': eye, 'Features': i, 'result': result},
        #                         partition=list(result['Partition']))

        # plot_scattered_data(X, list(results[0]['Results'][10]['Partition']))
        # plot_scattered_data(X)
bestResults = analyzeResults(allResults, list(featured_records.index))



insert_bestClusterings(conn, bestResults, featured_records)

print('END...')



