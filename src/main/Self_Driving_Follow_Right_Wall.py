import Self_Driving_Naive
import Control_BrickPi

import time

from src.main.old_test_scripts.Touch_Response_Testing import speed_left

STANDARD_SPEED = -25
TURN_SPEED = 15
DISTANCE_TO_WALL = 15


def self_driving(bp, pars):
    speed_left = 0
    speed_right = 0

    try:
        if Self_Driving_Naive.bumped_into_wall(bp):
            if detect_finish(bp):
                pars["mode"] = 0
            else:
                turn_left_after_bump(bp, pars)
                speed_left = 0
                speed_right = 0
        elif is_right_wall_found(bp):
            speed_left, speed_right = turn_left_on_bridge()
        elif red_line_found(bp):
            speed_left, speed_right = turn_left_on_bridge()
        else:
            speed_left, speed_right = turn_right()
    except:
        print("Invalid sensor data.")

    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)


def turn_left_after_bump(bp, pars):
    time.sleep(0.4)  # drive into wall to set it straight
    Self_Driving_Naive.reverse_after_bump(bp, pars)
    speed_left, speed_right = turn_left()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.65)


def is_right_wall_found(bp):
    return bp.get_sensor(bp.PORT_1) < DISTANCE_TO_WALL


def red_line_found(bp):
    return (bp.get_sensor(bp.PORT_4)[0] > 15) and (bp.get_sensor(bp.PORT_4)[1] < 5) and (
            bp.get_sensor(bp.PORT_4)[2] < 5)


def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right


def turn_right():
    speed_left = STANDARD_SPEED - TURN_SPEED
    speed_right = STANDARD_SPEED + TURN_SPEED
    return speed_left, speed_right


def turn_left_on_bridge():
    speed_left = STANDARD_SPEED + TURN_SPEED
    speed_right = STANDARD_SPEED - TURN_SPEED
    return speed_left, speed_right


def detect_black(bp):
    return (bp.get_sensor(bp.PORT_4)[0] < 5) and (bp.get_sensor(bp.PORT_4)[1] < 5) and (
            bp.get_sensor(bp.PORT_4)[2] < 5)


def detect_finish(bp):
    return detect_black(bp) and is_right_wall_found(bp)
