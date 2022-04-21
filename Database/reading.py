import pandas as pd

def read_featuredRecords(conn, groupId=-1):
    if groupId != -1:
        df = pd.read_sql_query(  #
            f"""
            SELECT
                recording_id, subject_id, group_id, fc, afd, fdmax, fdmin, fdt, fda, 
                sc, asd, sdmax, sdmin, sdt, sda, sat, asa, samax, samin, ssv, svmax, svmin, asl, 
                bc, bfc, bdt, bda, bdmax, bdmin, 
                spl, adt, adpff_right, adpff_left
            FROM featured_records_task_2515
                """,
            conn,
            index_col="recording_id")
    else:
        df = pd.read_sql_query()