#!/usr/bin/env python

from __future__ import print_function  # use python 3 syntax but make it compatible with python 2
from __future__ import division

import time  # import the time library for the sleep function
import brickpi3  # import the BrickPi3 drivers
import pygame

# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15

BP = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)

pygame.init()
pygame.display.set_mode((100, 100))

try:
    print("Use arrowkeys to control.")
    value = 0
    reversevalue = 0

    speedleft = 0
    speedright = 0
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
    while running:
        try:
            value = BP.get_sensor(BP.PORT_2)
            reversevalue = BP.get_sensor(BP.PORT_3)
        except brickpi3.SensorError as error:
            print(error)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                speedleft = 0
                speedright = 0
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

        if mode == 0:
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

        if mode == 8:
            if turntime > 0:
                turntime -= 1
            else:
                if justbumped:
                    justbumped = False
                    if (BP.get_sensor(BP.PORT_1) < 40):
                        turntime = 40
                        speedleft = 30
                        speedright = -30
                    else:
                        turntime = 40
                        speedleft = -30
                        speedright = 30


                if reversetime == 0:
                    speedleft = -60
                    speedright = -60
                else:
                    reversetime -= 1
                if (BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3)):
                    reversetime = 80
                    speedleft = 30
                    speedright = 30
                    justbumped = True




        else:

            try:
                print(BP.get_sensor(BP.PORT_4))
                print(BP.get_sensor(BP.PORT_1))
                if spaceIsPressed:
                    speedleft = -50
                    speedright = -50
                elif lshiftIsPressed:
                    speedleft = 0
                    speedright = 0
                elif (BP.get_sensor(BP.PORT_1) < 20) and mode == 1:
                    speedleft = 0
                    speedright = 0
                elif (BP.get_sensor(BP.PORT_2) or BP.get_sensor(BP.PORT_3)) and mode == 2:
                    speedleft = 0
                    speedright = 0
                elif (BP.get_sensor(BP.PORT_4)[0] > 90) and (BP.get_sensor(BP.PORT_4)[1] < 30) and (BP.get_sensor(BP.PORT_4)[2] < 30) and mode == 3:
                    speedleft = 0
                    speedright = 0
                elif (BP.get_sensor(BP.PORT_4)[0] < 30) and (BP.get_sensor(BP.PORT_4)[1] < 30) and (BP.get_sensor(BP.PORT_4)[2] < 30) and mode == 3:
                    speedleft = 0
                    speedright = 0
            except brickpi3.SensorError as error:
                print(error)


        # Set the motor speed for all four motors
        BP.set_motor_power(BP.PORT_D, speedleft)
        BP.set_motor_power(BP.PORT_A, speedright)
        BP.set_motor_power(BP.PORT_B, speedblade)

        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt:  # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()  # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.


