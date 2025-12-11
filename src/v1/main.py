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
leftDtOne = Motor(Ports.PORT19, GearSetting.RATIO_6_1, False)
leftDtTwo = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)
left_dt = MotorGroup(leftDtOne, leftDtTwo)

right_dt_one = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
right_dt_two = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
right_dt = MotorGroup(right_dt_one, right_dt_two)

dt = SmartDrive(left_dt, right_dt, gyro, wheelTravel = 260, units = DistanceUnits.MM)

# Motors
left_intake = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_intake = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
intake = MotorGroup(left_intake, right_intake)

flywheel = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
conveyor = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)  

# Pnuematics
tube_dispenser = DigitalOut(brain.three_wire_port.a)
descore = DigitalOut(brain.three_wire_port.b)

# Global Variables
auton_side = "R"
start_integral = 0
start_derivative = 0

isDriving = False


##################################################################### END HARDWARE DEFINITIONS #######################################################

def PID_drive(distance_degrees, heading, velocity, kP, kI, kD):
    global start_integral, start_derivative
    left_dt.set_position(0, DEGREES)
    right_dt.set_position(0, DEGREES)

    integral = start_integral
    derivative = start_derivative
    previousError = 0

    if velocity >= 0:
        while left_dt.position(DEGREES) < distance_degrees:
            # set error
            error = heading - gyro.rotation()

            # update integral
            integral += error
            integral = max(min(integral, 50), -50)

            # update derivative
            derivative = error - previousError
            derivative = max(min(derivative, 50), -50)

            #set velocities
            output = (kP * error) + (kI * integral) + (kD * derivative)

            left_dt.set_velocity((velocity + output), units = PERCENT)
            right_dt.set_velocity((velocity - output), units = PERCENT)
            left_dt.spin(FORWARD)
            right_dt.spin(FORWARD)

            previousError = error
            wait(100, MSEC)

    else:
        while left_dt.position(DEGREES) > distance_degrees:
            # set error
            error = heading - gyro.rotation()

            # update integral
            integral += error
            integral = max(min(integral, 50), -50)

            # update derivative
            derivative = error - previousError
            derivative = max(min(derivative, 50), -50)

            #set velocities
            output = (kP * error) + (kI * integral) + (kD * derivative)

            left_dt.set_velocity((velocity + output), units = PERCENT)
            right_dt.set_velocity((velocity - output), units = PERCENT)
            left_dt.spin(FORWARD)
            right_dt.spin(FORWARD)

            previousError = error

            wait(20, MSEC)

    #
    left_dt.stop()
    right_dt.stop()


    
def driver_control():
    """
    Code that runs when the user is controlling the robot 
    """
    isDriving = True
    while isDriving:
        # drivetrain
        if abs(controller_1.axis3.position()) >= 5 or abs(controller_1.axis1.position()) >= 5: # deadzone
            f_joystick = 0.5 * (float(controller_1.axis3.position()))
            t_joystick = 0.3 * (float(controller_1.axis1.position()))
            # left_drive_velocity = ((0.7 * (float(controller_1.axis3.position())) + (0.5 * float(controller_1.axis1.position()))))
            # right_drive_velocity = ((0.7 * float(controller_1.axis3.position()) - (0.5 * float(controller_1.axis1.position()))))
            left_drive_velocity = f_joystick + t_joystick
            right_drive_velocity= f_joystick - t_joystick

            if left_drive_velocity > 0:
                left_dt.set_velocity(abs(left_drive_velocity), units = PERCENT)
                left_dt.spin(FORWARD)
            else:                
                left_dt.set_velocity(abs(left_drive_velocity), units = PERCENT)
                left_dt.spin(REVERSE)
            if right_drive_velocity > 0:
                right_dt.set_velocity(abs(right_drive_velocity), units = PERCENT)
                right_dt.spin(FORWARD)
            else:                
                right_dt.set_velocity(abs(right_drive_velocity), units = PERCENT)
                right_dt.spin(REVERSE)
        else:
            dt.stop()

        # flywheel and conveyor belt
        if controller_1.buttonR1.pressing() and controller_1.buttonR2.pressing():
            flywheel.set_velocity(600)
            conveyor.spin(FORWARD)
            flywheel.spin(FORWARD)
        elif controller_1.buttonR2.pressing() and not(controller_1.buttonR1.pressing()):
            conveyor.spin(FORWARD)
            flywheel.stop()
        elif controller_1.buttonR1.pressing() and not(controller_1.buttonR2.pressing()):
            flywheel.set_velocity(600)
            conveyor.spin(REVERSE)
            flywheel.spin(FORWARD)
        else:
            flywheel.set_velocity(600)
            conveyor.set_velocity(600)
            conveyor.stop()
            flywheel.stop()

        # intake
        if controller_1.buttonL2.pressing():
            intake.spin(REVERSE, velocity = 600, units = RPM)
        elif controller_1.buttonL1.pressing():
            intake.spin(FORWARD, velocity = 600, units = RPM)
        else:
            intake.stop()
        
        # pneumatics
        if controller_1.buttonUp.pressing():
            tube_dispenser.set(True)
        elif controller_1.buttonDown.pressing():
            tube_dispenser.set(False)
        
        if controller_1.buttonX.pressing():
            descore.set(True)
        elif controller_1.buttonY.pressing():
            descore.set(False)
    isDriving = False

def autonomous():
    """
    ported code

    """
    if auton_side == "L":
        dt.set_drive_velocity(25, PERCENT)
        dt.set_turn_velocity(5, PERCENT)
        dt.set_stopping(BRAKE)
        intake.set_velocity(100, PERCENT)
        intake.spin(REVERSE)
        conveyor.set_velocity(100, PERCENT)
        conveyor.spin(FORWARD)
        flywheel.set_velocity(100, PERCENT)

        #dt.drive_for(FORWARD, 1300, MM)
        #PID_drive(1100, -4, 25, 0.2, 0.01, 0.01)

        dt.turn_to_rotation(-6)
        wait(20, MSEC)
        dt.drive_for(FORWARD, 1200, MM)

        wait(2, SECONDS)

        dt.drive_for(REVERSE, 600, MM)
        wait(250, MSEC)
        
        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(90, DEGREES)

        wait(150, MSEC)

        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(90, DEGREES)
        wait(250, MSEC)

        dt.drive_for(REVERSE, 800, MM)

        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(180, DEGREES)

        wait(150, MSEC)

        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(180, DEGREES)

        wait(150, MSEC)

        dt.drive_for(REVERSE, 250, MM)
        dt.drive(REVERSE)
        wait(500, MSEC)
        flywheel.spin(FORWARD)
        
        wait(2, SECONDS)

        flywheel.stop()
        dt.stop()



    elif auton_side == "R":
        dt.set_drive_velocity(25, PERCENT)
        dt.set_turn_velocity(5, PERCENT)
        dt.set_stopping(BRAKE)
        intake.set_velocity(100, PERCENT)
        intake.spin(REVERSE)
        conveyor.set_velocity(100, PERCENT)
        conveyor.spin(FORWARD)
        flywheel.set_velocity(100, PERCENT)

        #dt.drive_for(FORWARD, 1300, MM)
        #PID_drive(1100, -4, 25, 0.2, 0.01, 0.01)

        #dt.turn_to_rotation(4)
        wait(20, MSEC)
        dt.drive_for(FORWARD, 1200, MM)

        wait(2, SECONDS)

        dt.drive_for(REVERSE, 600, MM)
        wait(250, MSEC)
        
        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(-90, DEGREES)

        wait(150, MSEC)

        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(-90, DEGREES)
        wait(250, MSEC)

        dt.drive_for(REVERSE, 700, MM)

        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(-180, DEGREES)

        wait(150, MSEC)

        dt.set_turn_velocity(5, PERCENT)
        dt.turn_to_rotation(-180, DEGREES)

        wait(150, MSEC)

        dt.drive_for(REVERSE, 250, MM)
        dt.drive(REVERSE)
        wait(500, MSEC)
        flywheel.spin(FORWARD)
        
        wait(2, SECONDS)

        flywheel.stop()
        dt.stop()
    
    #dt.drive_for(REVERSE, 600, MM)


# delegates robot behavior during competitiondti
competition = Competition(driver_control, autonomous)

def main():
    """
    sets up and updates the UI
    """
    brain.screen.clear_screen()

    # set the text color 
    brain.screen.set_pen_color(Color.WHITE)

    # top right of the screen (where rows and columns are 1-index, NOT zero-indexed!)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("andy needs to read documentation") # print it once for lucas to see 

    # timer for stuff on the UI
    timer = Timer()   

    
    while True:
        #print temps
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(1, 1)
        controller_1.screen.print("L: " + str(leftDtOne.temperature()) + " " + str(leftDtTwo.temperature()) + " " + "R: " + str(right_dt_one.temperature()) + " " + str(right_dt_two.temperature()))
        
        #print rpms
        controller_1.screen.set_cursor(2, 1)
        controller_1.screen.print("I: " + str(int(intake.velocity())) + " " + "F: " + str(int(flywheel.velocity())) +" " + "C: " + str(int(conveyor.velocity())))
        
        #drivetrain rpms
        controller_1.screen.set_cursor(3, 1)
        controller_1.screen.print("L: " + str(int(leftDtOne.velocity())) + " " + str(int(leftDtTwo.velocity())) + " " + "R: " + str(int(right_dt_one.velocity())) + " " + str(int(right_dt_two.velocity())))
        wait(500)
main()