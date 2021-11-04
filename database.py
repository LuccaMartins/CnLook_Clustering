import psycopg2
import database_entities

cursor = None

def connect():
    """ query data from the vendors table """
    conn = None
    try:
        global cursor
        conn = psycopg2.connect(user='postgres', password='2021', host='localhost', database='candlook_hvl')
        if cursor is None:
            cursor = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def query(queryStr, asObjects):
    cursor.execute(queryStr)
    result = cursor.fetchall()
    if asObjects:
        return rowsToObjects(result, 'recording_entity')
    else:
        return result

def rowsToObjects(result, tablename):
    objects = []
    if tablename == 'recording_entity':
        for row in result:
            objects.append(database_entities.Recording_Entity(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
            ))
    return objects


def getRecordsByTaskId(taskId, asObjects=False):
    return query("SELECT * FROM recording_entity WHERE task_id = '" + taskId + "'", asObjects)
