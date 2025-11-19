"""
Actual program that runs on the vex brain
"""
# Library imports
import time
from vex import *
from random import randint

from vex import *


''' 
HARDWARE DEFINITIONS 
drivetrain using smartdrive instead simple drivetrain



'''


# Core controls 
brain=Brain()
controller_1 = Controller(PRIMARY)
gyro = Inertial(Ports.PORT10)

# Drivetrain
left_dt_one = Motor(Ports.PORT19, GearSetting.RATIO_6_1)
left_dt_two = Motor(Ports.PORT20, GearSetting.RATIO_6_1)
left_dt_motorgroup = MotorGroup(left_dt_one, left_dt_two)

right_dt_one = Motor(Ports.PORT11, GearSetting.RATIO_6_1)
right_dt_two = Motor(Ports.PORT12, GearSetting.RATIO_6_1)
right_dt_motorgroup = MotorGroup(right_dt_one, right_dt_two)

dt = SmartDrive(left_dt_motorgroup, right_dt_motorgroup, gyro, wheelTravel = 260, units = DistanceUnits.MM)

# Motors
left_intake = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_intake = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
intake_motorgroup = MotorGroup(left_intake, right_intake)

flywheel = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
conveyor = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)  



##################################################################### END HARDWARE DEFINITIONS #######################################################


def driver_control():
    """
    Code that runs when the user is controlling the robot 
    """
    # called every 5 millisecs to not fry CPU but keep robot responsive to users inputs 
    #   - while loop listens to users input
    while True:
        if abs(controller_1.axis1.position() >= 5): # deadzone
            left_drive_velocity = 600.0 * ((0.7 * (float(controller_1.axis1.position())) - float(controller_1.axis3.position())) / 100.0)
            left_dt_motorgroup.set_velocity(left_drive_velocity, units = RPM)
            right_drive_velocity = 600.0 * ((float(controller_1.axis1.position()) + float(controller_1.axis3.position())) / 100.0)
            right_dt_motorgroup.set_velocity(right_drive_velocity, units = RPM)
        else:
            dt.stop()
        if controller_1.buttonR1.pressing() and controller_1.buttonR2.pressing():
            flywheel.set_velocity(600)
            conveyor.spin(REVERSE)
            flywheel.spin(FORWARD)
        elif controller_1.buttonR2.pressing() and not(controller_1.buttonR1.pressing()):
            conveyor.spin(REVERSE)
            flywheel.stop()
        elif controller_1.buttonR1.pressing() and not(controller_1.buttonR2.pressing()):
            flywheel.set_velocity(600)
            conveyor.spin(FORWARD)
            flywheel.spin(FORWARD)
        else:
            flywheel.set_velocity(600)
            conveyor.set_velocity(600)
            conveyor.stop()
            flywheel.stop()


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
    brain.screen.print("you suck lucas") # print it once for lucas to see 

    # timer for stuff on the UI
    timer = Timer()   

    while True:
        if timer.time(SECONDS) >= 2:
            brain.screen.clear_screen()
            timer.clear()      # reset the timer back to 0

        x = randint(0, 480 - 1)
        y = randint(0, 240 - 1)
        brain.screen.print_at("you suck andy", x=x, y=y)

        # update the screen every 40 seconds
        wait(40, MSEC)

        # a new change



main()