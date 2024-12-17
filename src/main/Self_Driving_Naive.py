import time

import Control_BrickPi


def self_driving(bp, pars):
    if bumped_into_wall(bp):
        time.sleep(0.4)  # drive into wall to set it straight
        reverse_after_bump(bp, pars)
        turn_after_bump(bp)

    speed_left, speed_right = normal_driving_speed()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)


def normal_driving_speed(speed_left=-60, speed_right=60):
    return speed_left, speed_right


def bumped_into_wall(bp):
    return bp.get_sensor(bp.PORT_2) or bp.get_sensor(bp.PORT_3)


def reverse_after_bump(bp, pars):
    speed_left = -pars["standard_speed"]
    speed_right = -pars["standard_speed"]
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(0.40 * -30 / pars["standard_speed"])


def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right


def turn_right():
    speed_left = -30
    speed_right = 30
    return speed_left, speed_right


def turn_after_bump(bp):
    if bp.get_sensor(bp.PORT_1) < 60:
        speed_left, speed_right = turn_left()
    else:
        speed_left, speed_right = turn_right()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.65)  # let it turn for this amount of time
