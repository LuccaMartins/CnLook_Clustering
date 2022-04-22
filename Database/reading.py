import pandas as pd

def read_featuredRecords(conn, task, groupId=-1, subjectId=-1):
    if subjectId != -1:
        df = pd.read_sql_query(
            f"""
            SELECT
                 recording_id, task_id, group_id, subject_id, features
            FROM featured_records
            WHERE subject_id = {subjectId}
            AND is_valid = TRUE 
            """,
            conn,
            index_col="recording_id",
            )
    elif groupId != -1 and subjectId == -1:
        df = pd.read_sql_query(
            f"""
            SELECT
                 recording_id, task_id, group_id, subject_id, features
            FROM featured_records
            WHERE group_id = {groupId}
            AND is_valid = TRUE 
            """,
            conn,
            index_col="recording_id",
        )
    else:
        df = pd.read_sql_query(
            """
            SELECT
                 recording_id, task_id, group_id, subject_id, features
            FROM featured_records
            WHERE is_valid = TRUE 
            """,
            conn,
            index_col="recording_id",
        )

    return df
