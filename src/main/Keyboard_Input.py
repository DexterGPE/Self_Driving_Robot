from __future__ import print_function
from __future__ import division

import pygame
import Control_BrickPi


def initialize_pygame():
    pygame.init()
    pygame.display.set_mode((100, 100))


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
            Control_BrickPi.set_motor_power(bp, 0, 0)
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
    elif event.key == pygame.K_4:
        key_states["mode"] = 4
    elif event.key == pygame.K_5:
        key_states["mode"] = 5
    elif event.key == pygame.K_6:
        key_states["mode"] = 6
    elif event.key == pygame.K_7:
        key_states["mode"] = 7
    elif event.key == pygame.K_8:
        key_states["mode"] = 8
    elif event.key == pygame.K_9:
        key_states["mode"] = 9
    elif event.key == pygame.K_0:
        key_states["mode"] = 0
    return key_states
