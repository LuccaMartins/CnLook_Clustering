import database

database.connect()

records = database.getRecordsByTaskId('2510')

for rec in records:
    rec.print()