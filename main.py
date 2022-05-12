import serial
from app import App
from serialCom import init_serial

numMotors = 16
numFrames = 4
pattern_length2 = 20

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

arduino.flush()
init_serial(arduino, numMotors)
app = App([numMotors, 0, pattern_length2, numFrames])
app.mainloop()