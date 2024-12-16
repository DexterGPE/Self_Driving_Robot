import Control_BrickPi
import time

def celebration_1(bp):
    reverse(bp)

    turn_left(bp)
    reverse(bp)
    forward(bp)
    turn_right(bp)

    forward(bp)


def reverse(bp):
    left_speed = 30
    right_speed = 30
    blade_speed = 15
    Control_BrickPi.set_motor_power(bp, left_speed, right_speed)
    Control_BrickPi.set_blade_power(bp, blade_speed)
    time.sleep(1)

def forward(bp):
    left_speed = -30
    right_speed = -30
    blade_speed = 30
    Control_BrickPi.set_motor_power(bp, left_speed, right_speed)
    Control_BrickPi.set_blade_power(bp, blade_speed)
    time.sleep(1)

def turn_left(bp):
    left_speed = 30
    right_speed = -30
    blade_speed = 50
    Control_BrickPi.set_motor_power(bp, left_speed, right_speed)
    Control_BrickPi.set_blade_power(bp, blade_speed)
    time.sleep(1)

def turn_right(bp):
    left_speed = -30
    right_speed = 30
    blade_speed = 65
    Control_BrickPi.set_motor_power(bp, left_speed, right_speed)
    Control_BrickPi.set_blade_power(bp, blade_speed)
    time.sleep(1)