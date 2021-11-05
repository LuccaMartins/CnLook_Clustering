import psycopg2
import entities

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

def query(queryStr):
    cursor.execute(queryStr)
    result = cursor.fetchall()
    return result

def rowsToObjects(result, tablename):
    objects = []
    if tablename == 'recording_entity':
        for row in result:
            objects.append(entities.Recording_Entity(row))
    elif tablename == 'sample_entity':
        for row in result:
            objects.append((entities.Sample_Entity(row)))
    elif tablename == 'task_entity':
        for row in result:
            objects.append((entities.Task_Entity(row)))
    if len(objects) == 1: return objects[0]
    else: return objects

def getRecordById(recordId, asObject=False):
    result = query("SELECT * FROM recording_entity WHERE recording_id = '" + recordId + "'")
    if asObject:
        return rowsToObjects(result, 'recording_entity')
    else:
        return result

def getRecordsByTaskId(taskId, asObjects=False):
    result = query("SELECT * FROM recording_entity WHERE task_id = '" + taskId + "'")
    if asObjects:
        return rowsToObjects(result, 'recording_entity')
    else:
        return result

def getRecordSamples(recordId, asObjects=False):
    result = query("SELECT * FROM sample_entity WHERE recording_id = '" + recordId + "'")
    if asObjects:
        return rowsToObjects(result, 'sample_entity')
    else:
        return result

def getTaskById(taskId, asObject=False):
    result = query("SELECT * FROM task_entity WHERE id = '" + taskId + "'")
    if asObject:
        return rowsToObjects(result, 'task_entity')
    else:
        return result

def getTaskByRecordId(recordId, asObject):
    taskId = getRecordById(recordId, True).task_id
    result = query("SELECT * FROM task_entity WHERE id = '" + str(taskId) + "'")
    if asObject:
        return rowsToObjects(result, 'task_entity')
    else:
        return result