"""
Actual program that runs on the vex brain
"""
# Library imports
from vex import *
from robot_config import *

def driver_control():
    """
    Function that runs when the user is controlling the robot 
    """
    # called every 5 millisecs to not fry CPU but keep robot responsive to users inputs 
    #   - while loop listens to users input
    while True:
        left_motor.set_velocity((controller_1.axis3.position() + controller_1.axis1.position()), PERCENT)
        right_motor.set_velocity((controller_1.axis3.position() - controller_1.axis1.position()), PERCENT)
        left_motor.spin(FORWARD)
        right_motor.spin(FORWARD)
        wait(5, MSEC)

def autonomous():
    pass

def main():
    autonomous()
    driver_control()

main()