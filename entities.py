class Recording_Entity:
    def __init__(self, row):
        self.recording_id = row[0]
        self.name = row[1]
        self.date_created = row[2]
        self.calibration_id = row[3]
        self.timestamp_start = row[4]
        self.timestamp_end = row[5]
        self.notes = row[6]
        self.task_id = row[7]
        self.is_valid = row[8]
        self.screening_id = row[9]

    def print(self):
        print('- recording_id: ' + str(self.recording_id),
              ', name: ' + self.name,
              ', date_created: ' + str(self.date_created),
              ', calibration_id: ' + str(self.calibration_id),
              ', timestamp_start: ' + str(self.timestamp_start),
              ', timestamp_end: ' + str(self.timestamp_end),
              ', notes: ' + str(self.notes),
              ', task_id: ' + str(self.task_id),
              ', is_valid: ' + str(self.is_valid),
              ', screening_id: ' + str(self.screening_id))

class Sample_Entity:
    def __init__(self, row):
        self.sample_id = row[0]
        self.recording_id = row[1]
        self.timestamp = row[2]
        self.left_normal = row[3]
        self.right_normal = row[4]
        self.tracking_status = row[5]
        self.left_eye_position_x = row[6]
        self.left_eye_position_y = row[7]
        self.left_eye_position_z = row[8]
        self.right_eye_position_x = row[9]
        self.right_eye_position_y = row[10]
        self.right_eye_position_z = row[11]
        self.left_screen_coordinates = row[12]
        self.right_screen_coordinates = row[13]
        self.left_normalized_eye_position_in_track_box_x = row[14]
        self.left_normalized_eye_position_in_track_box_y = row[15]
        self.left_normalized_eye_position_in_track_box_z = row[16]
        self.right_normalized_eye_position_in_track_box_x = row[17]
        self.right_normalized_eye_position_in_track_box_y = row[18]
        self.right_normalized_eye_position_in_track_box_z = row[19]
        self.left_gaze_vector_x = row[20]
        self.left_gaze_vector_y = row[21]
        self.left_gaze_vector_z = row[22]
        self.right_gaze_vector_x = row[23]
        self.right_gaze_vector_y = row[24]
        self.right_gaze_vector_z = row[25]
        self.left_pupil_diameter_mm = row[26]
        self.right_pupil_diameter_mm = row[27]

    def print(self):
        print('- sample_id: ' + str(self.sample_id),
              ', recording_id: ' + str(self.recording_id),
              ', timestamp: ' + str(self.timestamp),
              ', left_normal: ' + str(self.left_normal),
              ', right_normal: ' + str(self.right_normal),
              ', tracking_status: ' + str(self.tracking_status),
              ', left_eye_position_x: ' + str(self.left_eye_position_x),
              ', left_eye_position_y: ' + str(self.left_eye_position_y),
              ', left_eye_position_z: ' + str(self.left_eye_position_z),
              ', right_eye_position_x: ' + str(self.right_eye_position_x),
              ', right_eye_position_y:' + str(self.right_eye_position_y),
              ', right_eye_position_z:' + str(self.right_eye_position_z),
              ', left_screen_coordinates:' + str(self.left_screen_coordinates),
              ', right_screen_coordinates:' + str(self.right_screen_coordinates),
              ', left_normalized_eye_position_in_track_box_x:' + str(self.left_normalized_eye_position_in_track_box_x),
              ', left_normalized_eye_position_in_track_box_y:' + str(self.left_normalized_eye_position_in_track_box_y),
              ', left_normalized_eye_position_in_track_box_z:' + str(self.left_normalized_eye_position_in_track_box_z),
              ', right_normalized_eye_position_in_track_box_x:' + str(self.right_normalized_eye_position_in_track_box_x),
              ', right_normalized_eye_position_in_track_box_y:' + str(self.right_normalized_eye_position_in_track_box_y),
              ', right_normalized_eye_position_in_track_box_z:' + str(self.right_normalized_eye_position_in_track_box_z),
              ', left_gaze_vector_x:' + str(self.left_gaze_vector_x),
              ', left_gaze_vector_y:' + str(self.left_gaze_vector_y),
              ', left_gaze_vector_z:' + str(self.left_gaze_vector_z),
              ', right_gaze_vector_x:' + str(self.right_gaze_vector_x),
              ', right_gaze_vector_y:' + str(self.right_gaze_vector_y),
              ', right_gaze_vector_z:' + str(self.right_gaze_vector_z),
              ', left_pupil_diameter_mm:' + str(self.left_pupil_diameter_mm),
              ', right_pupil_diameter_mm:' + str(self.right_pupil_diameter_mm))

class Task_Entity:
    def __init__(self, row):
        self.id = row[0]
        self.animation_blueprint = row[1]
        self.parameter_type = row[2]
        self.parameter_data = row[3]

    def print(self):
        print('- id: ' + str(self.id),
              ', animation_blueprint: ' + self.animation_blueprint,
              ', parameter_type: ' + str(self.parameter_type),
              ', parameter_data: ' + str(self.parameter_data))
