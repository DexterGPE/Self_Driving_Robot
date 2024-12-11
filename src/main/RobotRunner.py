from __future__ import print_function
from __future__ import division

import brickpi3
import pygame
import time

from Self_Driving_1 import *
from Manual_Driving import *


# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15

def initialize_keyboard_inputs():
    key_states = {
        "up": 0,
        "down": 0,
        "left": 0,
        "right": 0,
        "space": 0,
        "lshift": 0,
        "mode": 0
    }
    return key_states


def get_keyboard_input(key_states, running, bp):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            set_motor_power(bp, 0, 0)
            running = 0
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            key_states = get_key_pressed(event, key_states)
        elif event.type == pygame.KEYUP:
            key_states = get_key_released(event, key_states)

    return key_states, running


def get_key_released(event, key_states):
    if event.key == pygame.K_UP:
        key_states["up"] = 0
    elif event.key == pygame.K_DOWN:
        key_states["down"] = 0
    elif event.key == pygame.K_LEFT:
        key_states["left"] = 0
    elif event.key == pygame.K_RIGHT:
        key_states["right"] = 0
    elif event.key == pygame.K_SPACE:
        key_states["space"] = 0
    elif event.key == pygame.K_LSHIFT:
        key_states["lshift"] = 0
    return key_states


def get_key_pressed(event, key_states):
    if event.key == pygame.K_UP:
        key_states["up"] = 1
    elif event.key == pygame.K_DOWN:
        key_states["down"] = 1
    elif event.key == pygame.K_LEFT:
        key_states["left"] = 1
    elif event.key == pygame.K_RIGHT:
        key_states["right"] = 1
    elif event.key == pygame.K_SPACE:
        key_states["space"] = 1
    elif event.key == pygame.K_LSHIFT:
        key_states["lshift"] = 1
    elif event.key == pygame.K_1:
        key_states["mode"] = 1
    elif event.key == pygame.K_2:
        key_states["mode"] = 2
    elif event.key == pygame.K_3:
        key_states["mode"] = 3
    elif event.key == pygame.K_0:
        key_states["mode"] = 0
    elif event.key == pygame.K_8:
        key_states["mode"] = 8
    return key_states


def set_motor_power(bp, speed_left, speed_right):
    bp.set_motor_power(bp.PORT_D, speed_left)
    bp.set_motor_power(bp.PORT_A, speed_right)


def set_blade_power(bp, speed_blade):
    bp.set_motor_power(bp.PORT_B, speed_blade)


def initialize_brickpi_sensors():
    bp = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class.

    bp.set_sensor_type(bp.PORT_1, bp.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
    bp.set_sensor_type(bp.PORT_2, bp.SENSOR_TYPE.TOUCH)
    bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.TOUCH)
    bp.set_sensor_type(bp.PORT_4, bp.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)
    return bp


def initialize_pygame():
    pygame.init()
    pygame.display.set_mode((100, 100))


if __name__ == "__main__":
    running = True

    BP = initialize_brickpi_sensors()
    initialize_pygame()

    key_states = initialize_keyboard_inputs()

    while running:

        # check mode input van keyboard
        key_states, running = get_keyboard_input(key_states, running, BP)

        if key_states["mode"] == 0:
            manual_driving(BP, key_states)
        elif key_states["mode"] == 8:
            self_driving(BP)

        time.sleep(0.02)
