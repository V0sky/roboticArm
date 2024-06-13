#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from time import sleep
import uvicorn
import requests
import move
from move import CustomServo
import config
from config import ServoHomePositions
from config import Spray
from config import noEFmove
from config import ClawsEF
from config import EFRotation

app = FastAPI()
auto_setup = False

sources = config.ArmApi.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=sources,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def start_auto_setup():
    global auto_setup
    auto_setup = True
    print(f"Claws EF setup: {auto_setup}")

def cancel_auto_setup():
    global auto_setup
    auto_setup = False
    print(f"Claws EF setup: {auto_setup}")

def send_request():
    response = requests.get(config.ArmApi.request_URL)
    if response.status_code == config.ArmApi.status_code_successful:
        print("Successfuly requested! Sequence finished.")
    else:
        response.status_code == config.ArmApi.status_code_unsuccessful
        print("Request unsuccessful!")

# Get to the handle and spray on it
def test_move_bottle():
    if auto_setup == True:
        move.MoveWithoutEF.no_EF_move(Spray.J1_move, Spray.J2_move, Spray.J3_move, Spray.J4_move)
        sleep(5)
        move.SprayTheHandle.PullBottleHandler()
        sleep(4)
        move.MoveWithoutEF.no_EF_move(ServoHomePositions.base_servo_home_pos,
                                                ServoHomePositions.shoulder_servo_home_pos,
                                                ServoHomePositions.elbow_servo_home_pos,
                                                ServoHomePositions.wrist_servo_home_pos)
        
    sleep(5)

# One move with EF with no other joints --> no CLAWS!
# Change params in config
# Add delay between moves 
def test_move_4DOF_no_claws():
    if auto_setup == True:
        move.MoveWithoutEF.no_EF_move(noEFmove.J1_move, noEFmove.J2_move, 
                                      noEFmove.J3_move, noEFmove.J4_move)
        sleep(5)

# 1) Move with non-rot open claws
# 2) close them
# 3) Move somewhere else and open claws again
# 4) Loop it if needed or add more moves
def test_move_4DOF_claws():
    if auto_setup == True:
        move.MoveClaws.no_rot_claws(ClawsEF.no_rot_open)
        sleep(3)
        
        move.MoveWithoutEF.no_EF_move(noEFmove.J1_move, noEFmove.J2_move, 
                                      noEFmove.J3_move, noEFmove.J4_move)
        sleep(5)
                
        move.MoveClaws.no_rot_claws(ClawsEF.no_rot_close)
        sleep(3)
        
        move.MoveWithoutEF.no_EF_move(noEFmove.J1_move_2, noEFmove.J2_move_2, 
                                      noEFmove.J3_move_2, noEFmove.J4_move_2)
        sleep(5)
        
        move.MoveClaws.no_rot_claws(ClawsEF.no_rot_open)
        sleep(3)
        
        move.MoveWithoutEF.no_EF_move(noEFmove.J1_move_home, noEFmove.J2_move_home, 
                                noEFmove.J3_move_home, noEFmove.J4_move_home)
        sleep(5)

# 1) Move with rotational open claws
# 2) close them
# 3) Move somewhere else, rotate and open claws again
# 4) Loop it if needed or add more moves
def test_move_5DOF_claws():    
    move.MoveClaws.claws_with_rotation(ClawsEF.rot_open)
    sleep(3)
   
    move.MoveWithoutEF.no_EF_move(noEFmove.J1_move, noEFmove.J2_move, 
                                  noEFmove.J3_move, noEFmove.J4_move)
    
    move.MoveClaws.rotational_servo(EFRotation.J5_move_1)
    sleep(7)
    
    move.MoveClaws.claws_with_rotation(ClawsEF.rot_close)
    sleep(3)
    
    move.MoveWithoutEF.no_EF_move(noEFmove.J1_move_2, noEFmove.J2_move_2, 
                                  noEFmove.J3_move_2, noEFmove.J4_move_2)
    
    move.MoveClaws.rotational_servo(EFRotation.J5_move_2)
    sleep(7)
    
    move.MoveClaws.claws_with_rotation(ClawsEF.rot_open)
    sleep(3)

# Add methods and for any servo, chain them as you like
# Add delay when you need
def test_separated_custom():
    CustomServo.shoulder_servo_custom(config.CustomMovements.J2_custom)
    CustomServo.base_servo_custom(config.CustomMovements.J1_custom)
    CustomServo.wrist_servo_custom(config.CustomMovements.J4_custom)

# Sets autonomous control - API is active
@app.get("/autosetup/start")
def start_using_bottle_ef():
    start_auto_setup()

# Sets manual control - API is inactive
@app.get("/autosetup/cancel")
def cancel_using_bottle_ef():
    cancel_auto_setup()

# When requested, manipulator spray the door & send request outside (you can change URL in config)
@app.get("/tests/test1")
def test_move_1():
    test_move_bottle()
    send_request()

# When requested, manipulator moves with 4 DOF (no claws)
@app.get("/tests/test2")
def test_move_2():
    test_move_4DOF_no_claws()

# When requested, manipulator moves with 4 DOF (static claws)
@app.get("/tests/test3")
def test_move_3():
    test_move_4DOF_claws()

# When requested, manipulator moves with 5 DOF (rot claws)
@app.get("/tests/test4")
def test_move_4():
    test_move_5DOF_claws()

# Custom movements
@app.get("/tests/test5")
def test_separated_moves_():
    test_separated_custom()
    
        
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.50.98", port=8000, log_level = "info")