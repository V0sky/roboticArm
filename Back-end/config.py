class WsServerSettings:
    port = 3000
    positive_status_message = "Server is running.\nServer is listening on port 3000.\n"
    
class ServoHomePositions:
    base_servo_home_pos = 115
    shoulder_servo_home_pos = 0
    #shoulder_servo_home_pos = 32
    elbow_servo_home_pos = 180
    #elbow_servo_home_pos = 140
    wrist_servo_home_pos = 130
    rotation_servo_home_pos = 140
    claws_no_rotation_home_pos = 0
    claws_rotation_home_pos = 75
    bottle_servo_home_pos = 60
    
class ServoIndex:
    base_index = 0
    shoulder_index = 1
    elbow_index = 2
    wrist_index = 3
    rotational_index = 4
    claws_no_rot_index = 5
    claws_rot_index = 6
    bottle_index = 8
    
class ServoRanges:
    range_min = 0
    range_max = 180
    range_max_wrist = 300

    base_range_min_actual = 1
    base_range_max_actual = 179
    shoulder_range_min_actual = 32
    shoulder_range_max_actual = 140
    elbow_range_min_actual = 0
    elbow_range_max_actual = 135
    claws_no_rot_max = 65
    claws_rot_max = 80
    claws_rot_min_actual = 75
    claws_rot_max_actual = 155
    
class ElbowSmoothMove:
    moving_time = 3.3
    number_of_steps = 300
    backwards = 1
    forward = -1
    delay = 0.0025
    
class WristSmoothMove:
    moving_time = 2
    number_of_steps = 300
    backwards = -1
    forward = 1
    delay = 0.005
        
#def moves_for_test:
class RepeatbilityTest:
    bucket_1_J1_angle = 115
    bucket_1_J2_angle = 177
    bucket_1_J3_angle = 75
    bucket_1_J4_angle = 71
    
    bucket_2_J1_angle = 64
    bucket_2_J2_angle = 170
    bucket_2_J3_angle = 85
    bucket_2_J4_angle = 59
    
    bucket_3_J1_angle = 42
    bucket_3_J2_angle = 171
    bucket_3_J3_angle = 67
    bucket_3_J4_angle = 65
    
    shoulder_only = 120
    
class Spray:
    J1_move = 65
    J2_move = 77
    J3_move = 57
    J4_move = 200
    
    bottle_push = 178
    bottle_pull = 68

# Change or add more variables if needed for more complex movements
class noEFmove:
    J1_move_home = 115
    J2_move_home = 0
    J3_move_home = 180
    J4_move_home = 130
     
    J1_move = 115
    J2_move = 40
    J3_move = 120
    J4_move = 130
    
    J1_move_2 = 140
    J2_move_2 = 80
    J3_move_2 = 70
    J4_move_2 = 200
    
    J1_move_3 = 80
    J2_move_3 = 20
    J3_move_3 = 140
    J4_move_3 = 100

# Change as you need --> for endpoint /tests/test5
# Add more movements (e.g. J2_custom_2 = ...)
class CustomMovements:
    J1_custom = 115
    J2_custom = 0
    J3_custom = 180
    J4_custom = 130
    J5_custom = 140
    J6_custom = 0
    J7_custom = 0

class EFRotation:
    J5_move_1 = 70
    J5_move_2 = 140
    J5_move_3 = 70

class ClawsEF:
    no_rot_open = 0
    no_rot_close = 65
    rot_open = 0
    rot_close = 80

class ArmApi:
    origins =   [   "http://127.0.0.1:5500",
                    "http://192.168.50.97",
                    "http://192.168.50.98",
                ]
    
    request_URL = "https://api.github.com"
    status_code_successful = 200
    status_code_unsuccessful = 404