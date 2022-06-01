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
taskId = "2515"
print(f'Reading records from database ')

featured_records = read_featuredRecords(conn)

allResults = []
for i, eye in enumerate(eyes_combination):
    for j, subset in enumerate(subsets_of_features):
        X = shapeFeaturedRecords(featured_records, subsets_of_features.get(subset), eye)
        print(f"-> Test {i*len(subsets_of_features)+j+1} of {len(eyes_combination)*len(subsets_of_features)}")
        results = startClusteringTests(X)
        for result in results:
            result['Eye'] = eye
            result['Features Subset'] = subset
            allResults.append(result)

bestResults = analyzeResults(allResults, list(featured_records.index))


insert_bestClusterings(conn, bestResults, featured_records)

print('END...')



