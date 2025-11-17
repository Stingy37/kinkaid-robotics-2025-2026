"""
This module defines the hardware objects used elsewhere in the code
"""
from vex import *

# Core controls 
brain=Brain()
controller_1 = Controller(PRIMARY)
gyro = Gyro(brain.three_wire_port.a) # NOTE -> replace with actual port once gyro is implemented 

# ----------------------------------------- MOTORS -----------------------------------------
# example stuff
# Robot configuration code (MUST init robot's parts here for the while-loop below to work)
claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False) # in english, states that "claw_motor" is the motor at port3...
                                                               # now when we use this elsewhere in the code, we know WHAT part of the robot
                                                               # claw_motor controls 
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

# intake motors
left_intake = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_intake = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
intake_motorgroup = MotorGroup(left_intake, right_intake)

# drivetrain motors
left_dt_one = Motor(Ports.PORT19, GearSetting.RATIO_18_1)
left_dt_two = Motor(Ports.PORT20, GearSetting.RATIO_18_1)
left_dt_motorgroup = MotorGroup(left_dt_one, left_dt_two)

right_dt_one = Motor(Ports.PORT11, GearSetting.RATIO_18_1)
right_dt_two = Motor(Ports.PORT12, GearSetting.RATIO_18_1)
right_dt_motorgroup = MotorGroup(right_dt_one, right_dt_two)

dt = DriveTrain(left_dt_motorgroup, right_dt_motorgroup, 319.19, 295, 40, MM) # NOTE -> ask lucas / whoever's in charge about the settings here

# ------------------------------------- OTHER HARDWARE -----------------------------------------
flywheel = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False) # NOTE -> placeholder, wait for lucas to tell me what port actually 
                                                             # has the flywheel, OR maybe its a group OF motors
conveyor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)  
