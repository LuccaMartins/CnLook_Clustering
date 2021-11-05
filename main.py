import database
import json
import plotting

database.connect()

recordId = '764'
# records = database.getRecordsByTaskId('2510', True)
#
recordSamples = database.getRecordSamples(recordId, True)
#
# for sample in recordSamples:
#     sample.print()

# task = database.getTaskById('2515', True)
task = database.getTaskByRecordId(recordId, True)
# task.print()

taskJson = json.loads(task.animation_blueprint)

plotting.distanceToFigure_Horizontal(taskJson["NormalizedPositionDurations"], recordSamples)