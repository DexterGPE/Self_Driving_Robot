from __future__ import print_function
from __future__ import division

import time
import brickpi3
import pygame

# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15


def end_movement_when_closing_pygame(bp):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            set_motor_power(bp, 0, 0)
            set_blade_power(bp, 0)
    return running

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

def get_keyboard_input(key_states,running,bp):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            set_motor_power(bp, 0,0)
            running=0
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            key_states = get_key_pressed(event, key_states)
        elif event.type == pygame.KEYUP:
            key_states = get_key_released(event, key_states)

    return key_states,running

def get_key_released(event, key_states):
    if event.key == pygame.K_UP:
        print("up")
        key_states["up"] = 0
    elif event.key == pygame.K_DOWN:
        print("down")
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
        print("up")
        key_states["up"] = 1
    elif event.key == pygame.K_DOWN:
        print("down")
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
    bp = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

    bp.set_sensor_type(bp.PORT_1, bp.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
    bp.set_sensor_type(bp.PORT_2, bp.SENSOR_TYPE.TOUCH)
    bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.TOUCH)
    bp.set_sensor_type(bp.PORT_4, bp.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)
    return bp

def initialize_pygame():
    pygame.init()
    pygame.display.set_mode((100, 100))

def manual_driving(bp, key_states):
    speed_left = 0
    speed_right = 0
    speed_blade = 0
    print("in manual")

    if key_states["up"]:
        speed_left -= 60
        speed_right -= 60
    if key_states["down"]:
        speed_left += 60
        speed_right += 60
    if key_states["right"]:
        speed_right += 20
        speed_left -= 20
    if key_states["left"]:
        speed_right -= 20
        speed_left += 20
    if key_states["space"]:
        speed_blade = 100
    if key_states["lshift"]:
        speed_left = 0
        speed_right = 0
        speed_blade = 0

    set_motor_power(bp, speed_left, speed_right)
    set_blade_power(bp, speed_blade)

def bumped_into_wall():
    return BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3)

def reverse_after_bump():
    speed_left = 30
    speed_right = 30
    set_motor_power(BP, speed_left, speed_right)
    time.sleep(1) # let it reverse for this amount of time

def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right

def turn_right():
    speed_left = -30
    speed_right = 30
    return speed_left, speed_right

def turn_after_bump():
    if BP.get_sensor(BP.PORT_1) < 40:
        speed_left, speed_right = turn_left()
    else:
        speed_left, speed_right = turn_right()
    set_motor_power(BP, speed_left, speed_right)
    time.sleep(2) # let it turn for this amount of time

def normal_driving_speed():
    speed_left = -60
    speed_right = -60
    return speed_left, speed_right

def self_driving(bp):
    if bumped_into_wall():
        time.sleep(0.5)  # let it continue driving into wall for a bit to straighten it
        reverse_after_bump()
        turn_after_bump()

    speed_left, speed_right = normal_driving_speed()
    set_motor_power(bp, speed_left, speed_right)


if __name__ == "__main__":
    running = True

    BP = initialize_brickpi_sensors()
    initialize_pygame()

    key_states = initialize_keyboard_inputs()

    while running:

        # running = end_movement_when_closing_pygame(BP)

        # check mode input van keyboard
        key_states,running = get_keyboard_input(key_states,running,BP)

        if key_states["mode"] == 0:
            manual_driving(BP, key_states)
        elif key_states["mode"] == 8:
            self_driving(BP)

        time.sleep(0.02)
