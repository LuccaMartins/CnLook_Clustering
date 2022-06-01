import pandas as pd

def read_featuredRecords(conn, groupId=-1, subjectId=-1):
    if subjectId != -1:
        df = pd.read_sql_query(
            f"""
            SELECT
                 *
            FROM featured_records
            WHERE subject_id = {subjectId}
            AND is_valid = TRUE
            ORDER BY recording_id 
            """,
            conn,
            index_col="recording_id",
            )
    elif groupId != -1 and subjectId == -1:
        df = pd.read_sql_query(
            f"""
            SELECT
                 *
            FROM featured_records
            WHERE group_id = {groupId}
            AND is_valid = TRUE 
            ORDER BY recording_id 
            """,
            conn,
            index_col="recording_id",
        )
    else:
        df = pd.read_sql_query(
            """
            SELECT
                 *
            FROM featured_records
            WHERE is_valid = TRUE 
            ORDER BY recording_id 
            """,
            conn,
            index_col="recording_id",
        )

    return df
