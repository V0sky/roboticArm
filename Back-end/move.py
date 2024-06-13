from adafruit_servokit import ServoKit
from config import ServoRanges
from config import ServoIndex
import time
import config
import threading

class ServoInit:
    
    kit = ServoKit(channels=16)
    
    # J1 --> Base servo                 channel 0
    # J2 --> Shoulder servo             channel 1
    # J3 --> Elbow servo                channel 2
    # J4 --> Wrist servo                channel 3
    # J5 --> Rot-end effector servo     channel 4
    # J6 --> Claws - W/O rotation       cahnnel 5
    # J7 --> Claws - With rotation      channel 6
    # J8 --> Bottle end-effector        channel 7
    
    kit.servo[ServoIndex.base_index].set_pulse_width_range(600, 2400)
    kit.servo[ServoIndex.shoulder_index].set_pulse_width_range(600, 2400)
    kit.servo[ServoIndex.elbow_index].set_pulse_width_range(500, 2500)
    kit.servo[ServoIndex.wrist_index].set_pulse_width_range(600, 2400)
    kit.servo[ServoIndex.rotational_index].set_pulse_width_range(600, 2400)
    kit.servo[ServoIndex.claws_no_rot_index].set_pulse_width_range(600, 2400)
    kit.servo[ServoIndex.claws_rot_index].set_pulse_width_range(600, 2400)
    kit.servo[ServoIndex.bottle_index].set_pulse_width_range(600, 2400)

class MappingAngleValues:
    
    # To change value ranges according to the UI and any servo needs
    def servo_change_range_values(sent_num, in_min, in_max, out_min, out_max):
        return int(out_min + (int(sent_num - in_min) / int(in_max - in_min) * (out_max - out_min)))

    # Adjusted servo move range map with channel index
    def set_angle_to_channel(channel_index, angle, min_In, max_In, min_Out, max_Out):
        desired_angle = MappingAngleValues.servo_change_range_values(angle, min_In, max_In, min_Out, max_Out)
        ServoInit.kit.servo[channel_index].angle = desired_angle

# Global variables needed for updating position of two servos (J3 & J4) after each iteration
elbow_start_position = MappingAngleValues.servo_change_range_values(
                                                    config.ServoHomePositions.elbow_servo_home_pos,
                                                    ServoRanges.range_min, 
                                                    ServoRanges.range_max,
                                                    ServoRanges.elbow_range_min_actual, 
                                                    ServoRanges.elbow_range_max_actual)

wrist_start_position = MappingAngleValues.servo_change_range_values(
                                                    config.ServoHomePositions.wrist_servo_home_pos,
                                                    ServoRanges.range_min, ServoRanges.range_max_wrist,
                                                    ServoRanges.range_min, ServoRanges.range_max)
    
class SmoothServoMove:
        
    # Slow down J3(70KG) - microsteps, shorter transition, longer time for the whole move
    # end_position --> angle from a client
    # time_for_move --> param for creating microsteps
    # index --> param for control channel
    # delay --> delay between iterations
    def elbow_move_better(end_position, time_for_move, index):
        global elbow_start_position
        
        if end_position >= elbow_start_position:
            move_direction = config.ElbowSmoothMove.backwards
        else:
            move_direction = config.ElbowSmoothMove.forward
        
        move_distance = end_position - elbow_start_position
        move_distance = abs(move_distance)
        servo_steps_count = int(time_for_move * config.ElbowSmoothMove.number_of_steps)
        size_of_step = move_distance / servo_steps_count * move_direction
        
        for i in range (servo_steps_count):
            move_angle = elbow_start_position + size_of_step
            move_angle = min(max(move_angle, ServoRanges.elbow_range_min_actual), 
                            ServoRanges.elbow_range_max_actual)
            ServoInit.kit.servo[index].angle = move_angle
            elbow_start_position = move_angle
            time.sleep(config.ElbowSmoothMove.delay)

    # Slow down 300 degree wrist servo (with microsteps and smoother transition between pulses)     
    def wrist_move_better(end_position, time_for_move, index):
        global wrist_start_position
        
        if end_position >= wrist_start_position:
            move_direction = config.WristSmoothMove.forward
        else:
            move_direction = config.WristSmoothMove.backwards
        
        move_distance = end_position - wrist_start_position
        move_distance = abs(move_distance)
        servo_steps_count = int(time_for_move * config.WristSmoothMove.number_of_steps)
        size_of_step = move_distance / servo_steps_count * move_direction
        
        for i in range (servo_steps_count):
            move_angle = wrist_start_position + size_of_step
            move_angle = min(max(move_angle, ServoRanges.range_min), 
                            ServoRanges.range_max)
            ServoInit.kit.servo[index].angle = move_angle
            wrist_start_position = move_angle
            time.sleep(config.WristSmoothMove.delay)

class SprayTheHandle:
    def PullBottleHandler():
        for i in range (5):
            ServoInit.kit.servo[ServoIndex.bottle_index].angle = config.Spray.bottle_push
            time.sleep(0.5)
            ServoInit.kit.servo[ServoIndex.bottle_index].angle = config.Spray.bottle_pull
            time.sleep(0.5)
            ServoInit.kit.servo[ServoIndex.bottle_index].angle = config.Spray.bottle_push

# Methods for any servo separated (J1-J4)
# To be used primarily in custom endpoint /tests/test5
class CustomServo:
    def base_servo_custom(angle1):
        MappingAngleValues.set_angle_to_channel(config.ServoIndex.base_index, 
                        angle1, ServoRanges.range_min, 
                        ServoRanges.range_max, 
                        ServoRanges.base_range_min_actual,
                        ServoRanges.base_range_max_actual)
        
    def shoulder_servo_custom(angle2):
        MappingAngleValues.set_angle_to_channel(config.ServoIndex.shoulder_index, 
                        angle2, ServoRanges.range_min, 
                        ServoRanges.range_max, 
                        ServoRanges.shoulder_range_min_actual,
                        ServoRanges.shoulder_range_max_actual)
    
    def elbow_servo_custom(angle3):
        elbow_t = threading.Thread(target = SmoothServoMove.elbow_move_better, args =                   
        (MappingAngleValues.servo_change_range_values(angle3, ServoRanges.range_min, 
                        ServoRanges.range_max, 
                        ServoRanges.elbow_range_min_actual, 
                        ServoRanges.elbow_range_max_actual), 
                        config.ElbowSmoothMove.moving_time, 
                        config.ServoIndex.elbow_index),)
        elbow_t.start()
        
    def wrist_servo_custom(angle4):
        wrist_t = threading.Thread(target = SmoothServoMove.wrist_move_better, args =
        (MappingAngleValues.servo_change_range_values(angle4, ServoRanges.range_min, 
                        ServoRanges.range_max_wrist,
                        ServoRanges.range_min, ServoRanges.range_max),
                        config.WristSmoothMove.moving_time,
                        config.ServoIndex.wrist_index),)   
        wrist_t.start()
        
# Methods for claws movements & rotational servo J5
# To be used in custom endpoint /tests/test5
class MoveClaws:
    def no_rot_claws(angle6):
        MappingAngleValues.set_angle_to_channel(config.ServoIndex.claws_no_rot_index, 
                                angle6, ServoRanges.range_min, 
                                ServoRanges.range_max, 
                                ServoRanges.range_min,
                                ServoRanges.range_max)
    
    def rotational_servo(angle5):
        MappingAngleValues.set_angle_to_channel(config.ServoIndex.rotational_index, 
                                angle5, ServoRanges.range_min, 
                                ServoRanges.claws_no_rot_max, 
                                ServoRanges.range_min,
                                ServoRanges.claws_no_rot_max)
        
    def claws_with_rotation(angle7):
        MappingAngleValues.set_angle_to_channel(config.ServoIndex.claws_rot_index, 
                                angle7, ServoRanges.range_min, 
                                ServoRanges.claws_rot_max, 
                                ServoRanges.claws_rot_min_actual,
                                ServoRanges.claws_rot_max_actual)

# Complex move for 4DOF without Claws --> for ENDPOINTS
class MoveWithoutEF:      
    def no_EF_move(angle1, angle2, angle3, angle4):
        CustomServo.base_servo_custom(angle1)
        CustomServo.shoulder_servo_custom(angle2)
        CustomServo.elbow_servo_custom(angle3)
        CustomServo.wrist_servo_custom(angle4)