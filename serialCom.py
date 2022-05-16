import time

# Constants
CALIBRATE = 0
MOVE = 1
UP = 1
DOWN = 0
NOCALIBRATION = 0
CALIBRATION = 1

# Globals
arduino = None
numMotors = 0
motor_pos = []

def init_serial(serial, num_motors):
    global arduino, numMotors
    arduino = serial
    numMotors = num_motors
    for i in range(numMotors):
        motor_pos.append(-1)

def write_read(x):
    print("sent: " + x)
    arduino.write(bytes(x+"\n", 'utf-8'))
    time.sleep(0.2)
    data = ""
    while arduino.in_waiting:
        data += str(arduino.readline()) + "\n"
    return data

def get_message_str(motor, calibration, direction, mode):
    return str(motor << 3 | calibration << 2 | direction << 1 | mode)

def move_motor(motor, calibration, direction, mode):
    print(write_read(get_message_str(motor, calibration, direction, mode)))
    if mode == MOVE:
        motor_pos[motor-1] = direction

def calibrate_all():
    for i in range(numMotors):
        print(write_read(get_message_str(i+1, CALIBRATION, 0, 0)))
        motor_pos[i] = DOWN

def move_row(row):
    inds = [i for i, x in enumerate(row) if x == 1]
    for i in inds:
        if motor_pos[i] == DOWN:
            move_motor(i + 1, NOCALIBRATION, UP, MOVE)
    inds = [i for i, x in enumerate(row) if x == 0]
    for i in inds:
        if motor_pos[i] == UP:
            move_motor(i + 1, NOCALIBRATION, DOWN, MOVE)
    print(row)