import Self_Driving_Naive
import Control_BrickPi

import time

SMOOTHNESS = 5


def self_driving(bp):
    if Self_Driving_Naive.bumped_into_wall(bp):
        if detect_finish(bp):
            speed_left = 0
            speed_right = 0
        else:
            turn_left_after_bump(bp)
            speed_left = 0
            speed_right = 0
    elif red_line_found(bp):
        speed_left, speed_right = smooth_left_turn_on_bridge(speed_left, speed_right)
    elif get_right_wall_distance(bp) > 40:
        speed_left, speed_right = smooth_right_turn_on_bridge(speed_left, speed_right)
    else:
        speed_left, speed_right = smooth_turn_at_wall(bp)



    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)


def turn_left_after_bump(bp):
    time.sleep(0.4)  # drive into wall to set it straight
    Self_Driving_Naive.reverse_after_bump(bp)
    speed_left, speed_right = turn_left()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.65)


def is_right_wall_found(bp):
    return bp.get_sensor(bp.PORT_1) < 10

def get_right_wall_distance(bp):
    return bp.get_sensor(bp.PORT_1)

def smooth_turn_at_wall(bp):
    distance = get_right_wall_distance(bp)
    correction_factor = max(-1, min(1, (distance-10)/SMOOTHNESS))
    speed_left = -17.5 - 12.5 * correction_factor
    speed_right = -17.5 + 12.5 * correction_factor
    return speed_left, speed_right

def smooth_left_turn_on_bridge(speed_left, speed_right):
    speed_left = max(-5, speed_left + 12.5/(10*SMOOTHNESS))
    speed_right = max(-30, speed_right -12.5/(10*SMOOTHNESS))
    return speed_left, speed_right

def smooth_right_turn_on_bridge(speed_left, speed_right):
    speed_left = max(-30, speed_left -12.5/SMOOTHNESS)
    speed_right = max(-5, speed_right + 12.5/SMOOTHNESS)
    return speed_left, speed_right

def red_line_found(bp):
    return (bp.get_sensor(bp.PORT_4)[0] > 40) and (bp.get_sensor(bp.PORT_4)[1] < 20) and (
            bp.get_sensor(bp.PORT_4)[2] < 20)

def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right

def turn_right():
    speed_left = -30
    speed_right = -5
    return speed_left, speed_right

def turn_left_on_bridge():
    speed_left = -5
    speed_right = -30
    return speed_left, speed_right

def detect_black(bp):
    return (bp.get_sensor(bp.PORT_4)[0] < 20) and (bp.get_sensor(bp.PORT_4)[1] < 20) and (
            bp.get_sensor(bp.PORT_4)[2] < 20)

def detect_finish(bp):
    return detect_black(bp) and is_right_wall_found(bp)
