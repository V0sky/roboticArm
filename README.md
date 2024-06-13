# roboticArm
This project consists of front-end and back-end apps for manual as well as autonomous control of a robotic arm.

BACK-END
1) Arm_test.py:
   WebSocket server waiting for a JSON file from a GUI (mainly for manual control of the arm).
   
2) armapi.py:
   Rest-API for partially autonomous control of the arm. It consists of 7 end-points with prepared sequences of moves for any puproses user would like.

3) config.py:
   Pseudo-cofig file with a parameters for autonomous movements and for the user to change them in accordance with their needs.

4) led.py:
   File with a basic programme for LED light indication (neccessary for indicating that RPI is running as well as the servers on it).

5) move.py:
   A file with the core of all the servos' moves control.


FRONT-END
1) index.html:
   Mainpage for manual control.

2) index.js:
   Sliders and buttons functionality.

3) jsApi.js:
   For API requests purposes.

4) websoc.js:
   For creating JSON files sent via wesockets and GUI buttons functionality.

