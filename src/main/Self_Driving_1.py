import time

from RobotRunner import set_motor_power, set_blade_power


def normal_driving_speed():
    speed_left = -60
    speed_right = -60
    return speed_left, speed_right


def self_driving(bp):
    if bumped_into_wall(bp):
        time.sleep(0.4)  # drive into wall to set it straight
        reverse_after_bump(bp)
        turn_after_bump(bp)

    speed_left, speed_right = normal_driving_speed()
    set_motor_power(bp, speed_left, speed_right)


def bumped_into_wall(BP):
    return BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3)


def reverse_after_bump(BP):
    speed_left = 30
    speed_right = 30
    set_motor_power(BP, speed_left, speed_right)
    time.sleep(0.35)


def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right


def turn_right():
    speed_left = -30
    speed_right = 30
    return speed_left, speed_right


def turn_after_bump(BP):
    if BP.get_sensor(BP.PORT_1) < 40:
        speed_left, speed_right = turn_left()
    else:
        speed_left, speed_right = turn_right()
    set_motor_power(BP, speed_left, speed_right)
    time.sleep(1.65)  # let it turn for this amount of time
