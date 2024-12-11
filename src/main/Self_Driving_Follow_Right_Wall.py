import Self_Driving_Naive
import Control_BrickPi

import time

from src.main.old_test_scripts.Touch_Response_Testing import speed_right
from src.main.old_test_scripts.selfdriving_and_manual_but_not_working import speed_left


def self_driving(bp):
    if Self_Driving_Naive.bumped_into_wall(bp):
        turn_left_after_bump(bp)
        speed_left = 0
        speed_right = 0

    elif is_right_wall_found(bp):
        speed_left, speed_right = Self_Driving_Naive.normal_driving_speed()

    elif red_line_found(bp):
        speed_left, speed_right = turn_left()

    else:
        speed_left, speed_right = turn_right()

    # Zodra muur weg is, check of rode lijn gezien is
    # Geen muur, geen rood: ga naar rechts
    # Geen muur wel rood: tussen 2 rode lijnen blijven op de brug
    # Als hij botst, naar links gaan
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)


def turn_left_after_bump(bp):
    time.sleep(0.4)  # drive into wall to set it straight
    Self_Driving_Naive.reverse_after_bump(bp)
    speed_left, speed_right = turn_left()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.65)


def is_right_wall_found(bp):
    return bp.get_sensor(bp.PORT_1) < 40


def red_line_found(bp):
    return (bp.get_sensor(bp.PORT_4)[0] > 40) and (bp.get_sensor(bp.PORT_4)[1] < 20) and (
            bp.get_sensor(bp.PORT_4)[2] < 20)

def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right

def turn_right():
    speed_left = -30
    speed_right = 30
    return speed_left, speed_right