#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running all motors while a touch sensor connected to PORT_1 of the BrickPi3 is being pressed.
#
# Hardware: Connect EV3 or NXT motor(s) to any of the BrickPi3 motor ports. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, the motor(s) speed will ramp up and down while the touch sensor is pressed. The position for each motor will be printed.

from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division  # ''

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
# from inputs import get_key
import pygame

BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_1,
                   BP.SENSOR_TYPE.TOUCH)  # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)
pygame.init()
pygame.display.set_mode((100, 100))

try:
    print("Press touch sensor on port 1 to run motors")
    value = 0
    reversevalue = 0
    #    while (not value and not reversevalue):
    #        try:
    #            value = BP.get_sensor(BP.PORT_1)
    #            reversevalue = BP.get_sensor(BP.PORT_2)
    #        except brickpi3.SensorError:
    #            pass

    speedleft = 0
    speedright = 0
    leftIsPressed = 0
    rightIsPressed = 0
    upIsPressed = 0
    downIsPressed = 0
    while True:
        try:
            value = BP.get_sensor(BP.PORT_1)
            reversevalue = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError as error:
            print(error)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    upIsPressed = 1
                elif event.key == pygame.K_DOWN:
                    downIsPressed = 1
                if event.key == pygame.K_LEFT:
                    leftIsPressed = 1
                elif event.key == pygame.K_RIGHT:
                    rightIsPressed = 1
            speedleft = -30
            elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                upIsPressed = 0
            elif event.key == pygame.K_DOWN:
                downIsPressed = 0
            if event.key == pygame.K_LEFT:
                leftIsPressed = 0
            elif event.key == pygame.K_RIGHT:
                rightIsPressed = 0

        speedleft = 0
        speedright = 0
        if upIsPressed:
            speedleft += 20
            speedright += 20
        if downIsPressed:
            speedleft -= 20
            speedright -= 20
        if rightIsPressed:
            speedright += 20
            speedleft -= 20
        if leftIsPressed:
            speedright -= 20
            speedleft += 20

    # Set the motor speed for all four motors
    BP.set_motor_power(BP.PORT_D, speedleft)
    BP.set_motor_power(BP.PORT_A, speedright)

    #        try:
    #            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
    #            print("Encoder A: %6d  B: %6d  C: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C), BP.get_motor_encoder(BP.PORT_D)))
    #        except IOError as error:
    #            print(error)

    time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt:  # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()  # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
