#!/usr/bin/env python

from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import pygame

# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15

def setMotorPower(speed_left, speed_right, speed_blade):
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

def turn_left():
    turntime = 2
    speedleft = 26
    speedright = -26
    return turntime, speedright, speedleft

def turn_right():
    turntime = 2
    speedleft = -26
    speedright = 26
    return turntime, speedright, speedleft

def drive_backwards_after_bump():
    reversetime = 80
    speedleft = 30
    speedright = 30

    return reversetime, speedleft, speedright, justbumped

def selfDriving(turntime, justbumped, speedleft,speedright,reversetime,bumptime, stoppedbumping):
    if bumptime > 0:
        bumptime -= 1
        stoppedbumping = True if bumptime == 0 else False
    else:
        if stoppedbumping:
            reversetime, speedleft, speedright, justbumped = drive_backwards_after_bump()
            stoppedbumping = False

        if turntime > 0:
            turntime -= 1
        else:
            if reversetime == 0:
                justbumped = True

            else:
                reversetime -= 1

            if justbumped:
                justbumped = False
                if BP.get_sensor(BP.PORT_1) < 40:
                    turntime, speedright, speedleft = turn_left()
                else:
                    turntime, speedright, speedleft = turn_right()
            else:
                speedleft = -60
                speedright = -60



            if (BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3)):
                bumptime = 20


    return turntime, justbumped, speedleft,speedright,reversetime,bumptime, stoppedbumping

def manualDriving():
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
    return speed_right, speed_left, speed_blade

BP = initialize_brickpi_sensors()
initialize_pygame()


def get_key_board_input(running, speed_left, speed_right, upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
            speed_left = 0
            speed_right = 0
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
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
    return running, speed_left, speed_right, upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode


def get_pressure_sensor_input(value, reverse_value):
    try:
        value = BP.get_sensor(BP.PORT_2)
        reverse_value = BP.get_sensor(BP.PORT_3)
    except brickpi3.SensorError as error:
        print(error)
    return value, reverse_value


def sensor_testing_modes(speed_left, speed_right):
    print(BP.get_sensor(BP.PORT_4))
    print(BP.get_sensor(BP.PORT_1))
    if spaceIsPressed:
        speed_left = -50
        speed_right = -50
    elif lshiftIsPressed:
        speed_left = 0
        speed_right = 0
    elif (BP.get_sensor(BP.PORT_1) < 20) and mode == 1:
        speed_left = 0
        speed_right = 0
    elif (BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3)) and mode == 2:
        speed_left = 0
        speed_right = 0
    elif (BP.get_sensor(BP.PORT_4)[0] > 90) and (BP.get_sensor(BP.PORT_4)[1] < 30) and (
            BP.get_sensor(BP.PORT_4)[2] < 30) and mode == 3:
        speed_left = 0
        speed_right = 0
    elif (BP.get_sensor(BP.PORT_4)[0] < 30) and (BP.get_sensor(BP.PORT_4)[1] < 30) and (
            BP.get_sensor(BP.PORT_4)[2] < 30) and mode == 3:
        speed_left = 0
        speed_right = 0
    return speed_left, speed_right


try:
    print("Use arrowkeys to control.")
    value = 0
    reverse_value = 0
    speed_left = 0
    speed_right = 0
    speedblade = 0
    spaceIsPressed = 0
    upIsPressed = 0
    downIsPressed = 0
    leftIsPressed = 0
    rightIsPressed = 0
    lshiftIsPressed = 0
    justbumped = False
    turntime = 0
    running = 1
    mode = 0
    reversetime = 0
    stoppedbumping = False
    bumptime = 0


    while running:
        value, reverse_value = get_pressure_sensor_input(value, reverse_value)

        running, speed_left, speed_right, upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode = (
            get_key_board_input(running, speed_left, speed_right, upIsPressed, downIsPressed, leftIsPressed, rightIsPressed, spaceIsPressed, lshiftIsPressed, mode))

        if mode == 0:
            speed_right, speed_left, speedblade = manualDriving()

        if mode == 8:
            turntime, justbumped, speed_left,speed_right,reversetime, bumptime, stoppedbumping = selfDriving(turntime, justbumped, speed_left, speed_right, reversetime, bumptime, stoppedbumping)
        else:
            try:
                speed_left, speed_right = sensor_testing_modes(speed_left, speed_right)
            except brickpi3.SensorError as error:
                print(error)

        # Set the motor speed for all four motors
        setMotorPower(speed_left, speed_right, speedblade)

        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt:  # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()  # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.


