import Self_Driving_Naive
import Control_BrickPi

import time


def self_driving(bp):
    if Self_Driving_Naive.bumped_into_wall(bp):
        turn_left_after_bump(bp)
        speed_left = 0
        speed_right = 0
    elif is_right_wall_found(bp):
        speed_left, speed_right = Self_Driving_Naive.normal_driving_speed(-30, -30)
    elif red_line_found(bp):
        speed_left, speed_right = turn_left_on_bridge()
    else:
        speed_left, speed_right = turn_right()

    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)


def turn_left_after_bump(bp):
    time.sleep(0.4)  # drive into wall to set it straight
    Self_Driving_Naive.reverse_after_bump(bp)
    speed_left, speed_right = turn_left()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.65)


def is_right_wall_found(bp):
    return bp.get_sensor(bp.PORT_1) < 30


def red_line_found(bp):
    return (bp.get_sensor(bp.PORT_4)[0] > 40) and (bp.get_sensor(bp.PORT_4)[1] < 20) and (
            bp.get_sensor(bp.PORT_4)[2] < 20)


def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right


def turn_right():
    speed_left = -40
    speed_right = -5
    return speed_left, speed_right

def turn_left_on_bridge():
    speed_left = -10
    speed_right = -30
    return speed_left, speed_right