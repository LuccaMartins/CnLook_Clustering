import json
from Database.analysis import *

def insert_featuredRecords(conn, featuredRecords):
    sql = f"INSERT INTO featured_records(recording_id, task_id, group_name, subject_name, screening_date, screening_id, features, is_valid) " \
          f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # Execute the query for each record
    cursor = conn.cursor()
    for record in featuredRecords:
        recording_id = record['Record id']
        task_id, group_name, subject_name, screening_date, screening_id  = get_info_recording(conn, recording_id).values()
        cursor.execute(sql, (recording_id, task_id, group_name, subject_name, screening_date, screening_id,
                             json.dumps(record['Features']), True))
    conn.commit()



