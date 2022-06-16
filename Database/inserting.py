import json
from Database.analysis import *
# from Clustering_Framework.clustering_parameters import subsets_of_features

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def insert_featuredRecords(conn, featuredRecords):
    sql = f"INSERT INTO featured_records(recording_id, task_id, group_name, subject_name, screening_date, screening_id, features, is_valid) " \
          f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # Execute the query for each record
    cursor = conn.cursor()
    for record in featuredRecords:
        recording_id = record['Record id']
        print(f'Inserting record {recording_id}...')
        task_id, group_name, subject_name, screening_date, screening_id  = get_info_recording(conn, recording_id).values()
        cursor.execute(sql, (recording_id, task_id, group_name, subject_name, screening_date, screening_id,
                             json.dumps(record['Features']), True))
    conn.commit()

def insert_bestClusterings(conn, bestClusterings, featured_records):

    cursor = conn.cursor()
    for clustering in bestClusterings:
        sql = f"INSERT INTO clustering_results(method, method_info, partition, cluster_validation, features, data_recordings_ids)" \
              f"VALUES('{clustering['Method']}', " \
              f"'{json.dumps(clustering['Method Info'], cls=NumpyEncoder)}', " \
              f"'{json.dumps(clustering['Partition'], cls=NumpyEncoder)}'," \
              f"'{json.dumps(clustering['Cluster Validation'], cls=NumpyEncoder)}', " \
              f"'{json.dumps(clustering['Features Subset'], cls=NumpyEncoder)}', " \
              f"'{json.dumps(list(featured_records.index), cls=NumpyEncoder)}')"
        cursor.execute(sql)
    conn.commit()
