import json
from Database.analysis import *

def insert_featuredRecords(conn, featuredRecords):
    sql = f"INSERT INTO featured_records(recording_id, task_id, group_id, subject_id, screening_id, features) " \
          f"VALUES (%s, %s, %s, %s, %s, %s)"

    # Execute the query for each record
    cursor = conn.cursor()
    for record in featuredRecords:
        recording_id = record['Record id']
        info = get_info_recording(conn, recording_id)
        task_id, subject_id, group_id, screening_id = info.values()
        cursor.execute(sql, (recording_id, task_id, group_id, subject_id, screening_id, json.dumps(record['Features'])))
    conn.commit()

