"""
This module defines the hardware objects used elsewhere in the code
"""
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code (MUST init robot's parts here for the while-loop below to work)
claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False) # in english, states that "claw_motor" is the motor at port3...
                                                               # now when we use this elsewhere in the code, we know WHAT part of the robot
                                                               # claw_motor controls 
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)