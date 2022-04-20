import numpy as np
import pandas as pd

import scipy.interpolate
import scipy.stats
import scipy.signal

import sklearn.decomposition
from sklearn.base import BaseEstimator, TransformerMixin

import psycopg2

import ast

def insert_records(conn, featured_records):
    # Create a new record
    # sql = f"INSERT INTO `featured_records_task_2515` (`recording_id`, `subject_id`, " \
    #       f"`FC`, `AFD`, `FDMax`, `FDMin`, `FDT`, `FDA`," \
    #       f" `SC`, `ASC`, `SDMax`, `SDMin`, `SDT`, `SDA`, `SAT`, `ASA`, `SAMax`, `SAMin`, `SSV`, `SVMax`, `SVMin`, `ASL`," \
    #       f" `BC`, `BFC`, `BDT`, `BDA`, `BDMax`, `BDMin`," \
    #       f" `SPL`, `ADT`, `ADpFF_right`, `ADpFF_left`) " \
    #       f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
    #       f", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
    #       f", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
    #       f", %s, %s)"
    sql = f"INSERT INTO featured_records_task_2515 (recording_id, FC, AFD, FDMax, FDMin," \
          f" SC, ASD, SDMax, SDMin, ASL, " \
          f" ADT, ADpFF_right, ADpFF_left) " \
          f"VALUES (%s, %s, %s, %s, %s," \
          f"%s, %s, %s, %s, %s," \
          f"%s, %s, %s)"

    # Execute the query for each record
    cursor = conn.cursor()
    for record in featured_records:
        recording_id = record['Record id']
        # subject_id = 'NULL'
        FC = [record['Features'][0]['FC_left'], record['Features'][1]['FC_right']]
        AFD = [record['Features'][0]['AFD_left'], record['Features'][1]['AFD_right']]
        FDMax = [record['Features'][0]['FDMax_left'], record['Features'][1]['FDMax_right']]
        FDMin = [record['Features'][0]['FDMin_left'], record['Features'][1]['FDMin_right']]
        # FDT = [record['Features'][0]['FDT_left'], record['Features'][1]['FDT_right']]
        # FDA = [record['Features'][0]['FDA_left'], record['Features'][1]['FDA_right']]
        SC = [record['Features'][0]['SC_left'], record['Features'][1]['SC_right']]
        ASD = [record['Features'][0]['ASD_left'], record['Features'][1]['ASD_right']]
        SDMax = [record['Features'][0]['SDMax_left'], record['Features'][1]['SDMax_right']]
        SDMin = [record['Features'][0]['SDMin_left'], record['Features'][1]['SDMin_right']]
        # SDT = [record['Features'][0]['SDT_left'], record['Features'][1]['SDT_right']]
        # SDA = [record['Features'][0]['SDA_left'], record['Features'][1]['SDA_right']]
        # SAT = [record['Features'][0]['SAT_left'], record['Features'][1]['SAT_right']]
        # ASA = [record['Features'][0]['ASA_left'], record['Features'][1]['ASA_right']]
        # SAMax = [record['Features'][0]['SAMax_left'], record['Features'][1]['SAMax_right']]
        # SAMin = [record['Features'][0]['SAMin_left'], record['Features'][1]['SAMin_right']]
        # SSV = [record['Features'][0]['SSV_left'], record['Features'][1]['SSV_right']]
        # SVMax = [record['Features'][0]['SVMax_left'], record['Features'][1]['SVMax_right']]
        # SVMin = [record['Features'][0]['SVMin_left'], record['Features'][1]['SVMin_right']]
        ASL = [record['Features'][0]['ASL_left'], record['Features'][1]['ASL_right']]
        # BC = [record['Features'][0]['BC_left'], record['Features'][1]['BC_right']]
        # BFC = [record['Features'][0]['BFC_left'], record['Features'][1]['BFC_right']]
        # BDT = [record['Features'][0]['BDT_left'], record['Features'][1]['BDT_right']]
        # BDA = [record['Features'][0]['BDA_left'], record['Features'][1]['BDA_right']]
        # BDMax = [record['Features'][0]['BDMax_left'], record['Features'][1]['BDMax_right']]
        # BDMin = [record['Features'][0]['BDMin_left'], record['Features'][1]['BDMin_right']]
        # SPL = [record['Features'][0]['SPL_left'], record['Features'][1]['SPL_right']]
        ADT = [record['Features'][0]['ADT_left'], record['Features'][1]['ADT_right']]
        ADpFF_left = record['Features'][0]['ADpFF_left']
        ADpFF_right = record['Features'][1]['ADpFF_right']

        cursor.execute(sql, (recording_id, FC, AFD, FDMax, FDMin, \
                             SC, ASD, SDMax, SDMin, ASL, \
                             ADT, ADpFF_right, ADpFF_left
                             ))

    # the connection is not autocommited by default. So we must commit to save our changes.
    conn.commit()