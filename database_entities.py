class Recording_Entity:
    def __init__(self, recording_id, name, date_created, timestamp_start, timestamp_end, notes, task_id, is_valid, screening_id):
        self.recording_id = recording_id
        self.name = name
        self.date_created = date_created
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.notes = notes
        self.task_id = task_id
        self.is_valid = is_valid
        self.screening_id = screening_id

    def print(self):
        print('- recording_id: ' + str(self.recording_id),
              ',name: ' + self.name,
              ',date_created: ' + str(self.date_created),
              ',timestamp_start: ' + str(self.timestamp_start),
              ',timestamp_end: ' + str(self.timestamp_end),
              ',notes: ' + str(self.notes),
              ',task_id: ' + str(self.task_id),
              ',is_valid: ' + str(self.is_valid),
              ',screening_id: ' + str(self.screening_id))