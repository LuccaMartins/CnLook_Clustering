import pandas as pd

from Clustering_Framework.RecordSelection.record_selection import *
from Database.analysis import *
from Database.inserting import *
from Clustering_Framework.utils import *
from Database.visualization import *

#Connecting to database
print("Connecting to CnLook Database...")
conn = connect_db("127.0.0.1", "cnlook_")
taskId = 2515
print(f'Reading records from database (all tasks similar to Task {taskId})')
# records = list(getRecordings_SameTasks(conn))
records = getRecordings_SameTasks(conn)
print(f'Exporting data to csv file')
# df = pd.DataFrame(records)
records.to_csv('cnl_data.csv', encoding='utf-8')
print(f'Exportation finished.')




