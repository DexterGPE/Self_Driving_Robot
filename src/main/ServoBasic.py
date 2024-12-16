#!/usr/bin/env python

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import pygame

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)
pygame.init()
pygame.display.set_mode((100,100))

try:
    print("Use arrowkeys to control.")
    value = 0
    reversevalue = 0
    
    speedleft = 0
    speedright = 0
    speedblade = 0
    leftIsPressed = 0
    rightIsPressed = 0
    upIsPressed = 0
    downIsPressed = 0
    spaceIsPressed = 0
    running = 1
    while running:
        try:
            value = BP.get_sensor(BP.PORT_1)
            reversevalue = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError as error:
            print(error)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
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
                    
            speedleft = 0
            speedright = 0
            speedblade = 0
            if upIsPressed:
                speedleft -= 60
                speedright -= 60
            if downIsPressed:
                speedleft += 60
                speedright += 60
            if rightIsPressed:
                speedright += 20
                speedleft -= 20
            if leftIsPressed:
                speedright -= 20
                speedleft += 20
            if spaceIsPressed:
                speedblade = 200
        
        # Set the motor speed for all four motors
        BP.set_motor_power(BP.PORT_D, speedleft)
        BP.set_motor_power(BP.PORT_A, speedright)
        BP.set_motor_power(BP.PORT_B, speedblade)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the
                            # BrickPi3 firmware.


