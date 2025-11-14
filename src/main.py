"""
Actual program that runs on the vex brain
"""
# Library imports
from vex import *
from robot_config import *


# Begin project code
# Main Controller loop to set motors to controller axis postiions
while True:
    left_motor.set_velocity((controller_1.axis3.position() + controller_1.axis1.position()), PERCENT)
    right_motor.set_velocity((controller_1.axis3.position() - controller_1.axis1.position()), PERCENT)
    left_motor.spin(FORWARD)
    right_motor.spin(FORWARD)
    wait(5, MSEC)
