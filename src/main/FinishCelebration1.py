import ControlBrickPi
import time


def celebration_1(bp):
    reverse(bp)

    turn_left(bp)
    turn_right(bp)
    turn_left(bp)
    forward(bp)
    reverse(bp)
    turn_right(bp)
    turn_left(bp)
    turn_right(bp)
    forward(bp)


def reverse(bp):
    left_speed = 30
    right_speed = 30
    blade_speed = 15
    ControlBrickPi.set_motor_power(bp, left_speed, right_speed)
    ControlBrickPi.set_blade_power(bp, blade_speed)
    time.sleep(0.5)


def forward(bp):
    left_speed = -30
    right_speed = -30
    blade_speed = 30
    ControlBrickPi.set_motor_power(bp, left_speed, right_speed)
    ControlBrickPi.set_blade_power(bp, blade_speed)
    time.sleep(0.5)


def turn_left(bp):
    left_speed = 30
    right_speed = -30
    blade_speed = 50
    ControlBrickPi.set_motor_power(bp, left_speed, right_speed)
    ControlBrickPi.set_blade_power(bp, blade_speed)
    time.sleep(1)


def turn_right(bp):
    left_speed = -30
    right_speed = 30
    blade_speed = 65
    ControlBrickPi.set_motor_power(bp, left_speed, right_speed)
    ControlBrickPi.set_blade_power(bp, blade_speed)
    time.sleep(1)
