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
print(f'{len(featured_records)} recordings to cluster')


goodResults = []
for i, eye in enumerate(eyes_combination):
    subsets_of_features = createSubsetsOfFeatures(featured_records, eye)
    test = 1
    for j, subset in enumerate(subsets_of_features):
        X = shapeFeaturedRecords(featured_records, subset, eye)
        print(f"\n-> Test {test} of {len(subsets_of_features)} for {eye} eye")
        results = startClusteringTests(X)
        test += 1
        for result in results:
            result['Eye'] = eye
            result['Features Subset'] = subset
            if goodClustering(result, list(featured_records.index)):
                goodResults.asppend(result, list(featured_records.index))

# bestResults = analyzeResults(goodResults, list(featured_records.index))

# objects_pairwise_frequency, means = getObjectsPairwiseFrequency(bestResults, rec_ids)
# plot_pairwise_frequency_info(objects_pairwise_frequency, means, rec_ids, savePlot=True)

insert_bestClusterings(conn, goodResults, featured_records)

print('END...')



