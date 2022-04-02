import serial
import time

# connecting to serial port; only done once at the initialization of the GUI
arduino = serial.Serial(port='com8', baudrate=9600, timeout=0.1)
time.sleep(3)

# data to send, converted into strings to simplify communication
motor = str('c') # direction, down/up -> puncture (p/o), dispenser (d/c), rotary(r/q)
fullSteps=str(600)
halfSteps =str(0)
quarterSteps =str(0)

# sending data through the connected COM port
send = motor + fullSteps + ";"+ halfSteps + ";"+ quarterSteps + ";k"
arduino.write(send.encode())
time.sleep(1)

while (arduino.inWaiting() > 0):
    x = arduino.readline()
    print(x.decode('utf-8'))