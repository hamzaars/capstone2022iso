# capstone2022iso

**main.py** contains the GUI code and communication code

It needs the VotTracker.py in the same folder to run which keeps count of the currect volume in the syringe

**commTest.py** is used to troubleshoot the communcation

In order to run commTest.py and main.py, you need a eligible COM port (e.g. USB port) and need to specify which one it is and have it connected to the Arduino board

**forBoard.ino** is the main file uploaded onto the Arduino board to run the prototype

Please note, if you want to run the Arduino directly from this code (i.e. not using the main.py code), then the information to send to the serial port must be in this format: d100;20;50k (this is an example to run the dispenser motor 100 full steps, 20 half steps, and 50 quarter steps)

Refer to Section 2.3.4 Data Transfer for all possible combinations

This prototype code will only run d, c, p, o, x, and y

**motorcodefunctions_v3.ino** is used to troubleshoot the motors
