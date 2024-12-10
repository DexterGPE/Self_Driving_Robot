from __future__ import print_function
from __future__ import division

import time
import brickpi3
import pygame

# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15


def end_movement_when_closing_pygame(BP):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            setMotorPower(BP, 0, 0, 0)
    return running


def get_key_board_input(upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                upIsPressed = 1
            if event.key == pygame.K_DOWN:
                downIsPressed = 1
            if event.key == pygame.K_LEFT:
                leftIsPressed = 1
            if event.key == pygame.K_RIGHT:
                rightIsPressed = 1
            if event.key == pygame.K_SPACE:
                spaceIsPressed = 1
            if event.key == pygame.K_LSHIFT:
                lshiftIsPressed = 1
            if event.key == pygame.K_1:
                mode = 1
            if event.key == pygame.K_2:
                mode = 2
            if event.key == pygame.K_3:
                mode = 3
            if event.key == pygame.K_0:
                mode = 0
            if event.key == pygame.K_8:
                mode = 8
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                upIsPressed = 0
            if event.key == pygame.K_DOWN:
                downIsPressed = 0
            if event.key == pygame.K_LEFT:
                leftIsPressed = 0
            if event.key == pygame.K_RIGHT:
                rightIsPressed = 0
            if event.key == pygame.K_SPACE:
                spaceIsPressed = 0
            if event.key == pygame.K_LSHIFT:
                lshiftIsPressed = 0
    return upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode

def setMotorPower(BP, speed_left, speed_right, speed_blade):
    BP.set_motor_power(BP.PORT_D, speed_left)
    BP.set_motor_power(BP.PORT_A, speed_right)
    BP.set_motor_power(BP.PORT_B, speed_blade)

def initialize_brickpi_sensors():
    BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
    BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)
    BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
    BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)
    return BP

def initialize_pygame():
    pygame.init()
    pygame.display.set_mode((100, 100))

def manualDriving(BP, upIsPressed, downIsPressed, rightIsPressed,leftIsPressed,spaceIsPressed):
    speed_left = 0
    speed_right = 0
    speed_blade = 0

    if upIsPressed:
        speed_left -= 60
        speed_right -= 60
    if downIsPressed:
        speed_left += 60
        speed_right += 60
    if rightIsPressed:
        speed_right += 20
        speed_left -= 20
    if leftIsPressed:
        speed_right -= 20
        speed_left += 20
    if spaceIsPressed:
        speed_blade = 200

    setMotorPower(BP, speed_left, speed_right, speed_blade)


def selfDriving():
    # ipv variables voor tijd afwachten in loop gewoon sleeptime doen en dan weer door
    pass


if __name__ == "__main__":
    running = True

    BP = initialize_brickpi_sensors()
    initialize_pygame()

    while running:

        running = end_movement_when_closing_pygame(BP)

        # check mode input van keyboard
        upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode = get_key_board_input(upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode)

        if mode == 0:
            manualDriving(BP, upIsPressed, downIsPressed, rightIsPressed,leftIsPressed,spaceIsPressed)
        elif mode == 8:
            selfDriving()

        time.sleep(0.02)
