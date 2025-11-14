# ----------------------------------------------------------------------------- #
#                                                                               #                                    
#    Project:        Split Arcade Control                                       #                             
#    Module:         main.py                                                    #
#    Author:         VEX                                                        #
#    Created:        Fri Aug 05 2022                                            #
#    Description:    This example will use the left Y and right X               #
#                    Controller axis to control the Clawbot.                    #
#                                                                               #                                    
#    Configuration:  V5 Clawbot (Individual Motors)                             #
#                    Controller                                                 #
#                    Claw Motor in Port 3                                       #
#                    Arm Motor in Port 8                                        #
#                    Left Motor in Port 1                                       #
#                    Right Motor in Port 10                                     #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

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
