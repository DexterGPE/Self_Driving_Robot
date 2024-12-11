#!/usr/bin/env python

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import pygame

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
pygame.init()
pygame.display.set_mode((100,100))

try:
    print("Use arrowkeys to control.")
    value = 0
    reverse_value = 0
    
    speed_left = 0
    speed_right = 0
    speedblade = 0
    spaceIsPressed = 0
    running = 1
    reversetime = 0
    while running:
        try:
            value = BP.get_sensor(BP.PORT_2)
            reverse_value = BP.get_sensor(BP.PORT_3)
        except brickpi3.SensorError as error:
            print(error)
            
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
            
        if spaceIsPressed:
            speed_left = 0
            speed_right = 0
        elif reversetime == 0:
            speed_left = -30
            speed_right = -30
        elif BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3):
            reversetime = 30
            speed_left = 30
            speed_right = 30
        reversetime -=1
        
        # Set the motor speed for all four motors
        BP.set_motor_power(BP.PORT_D, speed_left)
        BP.set_motor_power(BP.PORT_A, speed_right)
        BP.set_motor_power(BP.PORT_B, speedblade)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.


