import json
import websockets
import asyncio
import config
from config import ServoHomePositions
import move

port = config.WsServerSettings.port
server_message = config.WsServerSettings.positive_status_message
         
# Move the servos
def set_servo_angles(angle1, angle2, angle3, 
                     angle4, angle5, angle6, angle7):
        
        move.CustomServo.base_servo_custom(angle1)
        move.CustomServo.shoulder_servo_custom(angle2)
        move.CustomServo.elbow_servo_custom(angle3)
        move.CustomServo.wrist_servo_custom(angle4)
        move.MoveClaws.rotational_servo(angle5)
        move.MoveClaws.no_rot_claws(angle6)
        move.MoveClaws.claws_with_rotation(angle7)
        
# To unload angle values got from a user & call function for moving servos
# with unloaded parameters
def unpack_json_angles(json_angles):
    s1_angle = json_angles["s1"]
    s2_angle = json_angles["s2"]
    s3_angle = json_angles["s3"]
    s4_angle = json_angles["s4"]
    s5_angle = json_angles["s5"]
    s6_angle = json_angles["s6"]
    s7_angle = json_angles["s7"]
    
    set_servo_angles(s1_angle, s2_angle, s3_angle, s4_angle,
                             s5_angle, s6_angle, s7_angle)
    
# Function for home positioning if an error occurs
def set_home_position():
        set_servo_angles(ServoHomePositions.base_servo_home_pos, 
                         ServoHomePositions.shoulder_servo_home_pos,
                         ServoHomePositions.elbow_servo_home_pos,
                         ServoHomePositions.wrist_servo_home_pos,
                         ServoHomePositions.rotation_servo_home_pos,
                         ServoHomePositions.claws_no_rotation_home_pos,
                         ServoHomePositions.claws_rotation_home_pos)

# Function with a loop for listening to new messages/events (receiving angles from a client)
# Handing the JSON to a function for unloading in
async def websocket_server(websocket):
    
    await websocket.send(f"{server_message}")
        
    try:
        while True:
            received_json = await websocket.recv()
            servo_angles = json.loads(received_json)
         
            unpack_json_angles(servo_angles)             
    
    except websockets.ConnectionClosedError:
        set_home_position()
        print("Internal Server Error.")

# Starting a server on a particular (or non-particular) adress and port
# Let the server run indefinetely (keyboard interruption possible)
server_start = websockets.serve(websocket_server, "", port)
asyncio.get_event_loop().run_until_complete(server_start) 
asyncio.get_event_loop().run_forever()