import database
import json
import plotter

database.connect()

#records = database.getRecordsByTaskId('2510', True)
#
#recordSamples = database.getRecordSamples(recordId, True)
#
# for sample in recordSamples:
#     sample.print()

# task = database.getTaskById('2515', True)
#task = database.getTaskByRecordId(recordId, True)
# task.print()
#
# record = database.getRecordById('701', True)
#
# [leftDist, rightDist] = record.distanceToFigure_Horizontal()
# plotting.distanceToFigure_Horizontal(record.timestamps, leftDist, rightDist)

#plotting.distanceToFigure_Horizontal(taskJson["NormalizedPositionDurations"], recordSamples)

recordId = '792'
objRecord = database.getRecordById(recordId)

objRecord.print()

# not working properly
# plotter.distanceToFigure_HV(objRecord)

plotter.positions_HV(objRecord)



