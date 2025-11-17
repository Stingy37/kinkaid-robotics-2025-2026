"""
Actual program that runs on the vex brain
"""
# Library imports
import time
from vex import *
from robot_config import * # imports all the hardware definitions for the robot


def driver_control():
    """
    Code that runs when the user is controlling the robot 
    """
    # called every 5 millisecs to not fry CPU but keep robot responsive to users inputs 
    #   - while loop listens to users input
    while True:
        pass


def autonomous():
    """
    Code that runs when the robot is in auton mode
    """
    # --- initial calibration
    gyro.calibrate() 
    dt.set_drive_velocity(50, PERCENT)
    dt.set_turn_velocity(50, PERCENT)


    # ---- move robot 
    intake_motorgroup.set_velocity(25, PERCENT)
    intake_motorgroup.spin(FORWARD)
    time.sleep(.25)

    intake_motorgroup.set_velocity(100, PERCENT)
    intake_motorgroup.spin(REVERSE)

    # ---- pick up items
    flywheel.set_velocity(50, PERCENT)
    conveyor.spin(REVERSE)
    flywheel.spin(FORWARD)

# delegates robot behavior during competition
competition = Competition(autonomous, driver_control)

def main():
    """
    sets up and updates the UI
    """
    brain.screen.clear_screen()

    # set the text color 
    brain.screen.set_pen_color(Color.WHITE)

    # top right of the screen (where rows and columns are 1-index, NOT zero-indexed!)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("you suck lucas")

    while True:
        # update UI
        wait(20, MSEC) 

main()