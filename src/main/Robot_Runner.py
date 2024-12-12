import time

import Self_Driving_Naive
import Self_Driving_Follow_Right_Wall
import Manual_Driving
import Keyboard_Input
import Control_BrickPi
import Smooth_Operator

# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15


def print_sensors(bp, countdown):
    if countdown == 0:
        print("Wall distance: {0}".format(bp.get_sensor(bp.PORT_1)))
        print("Color: {0}".format(bp.get_sensor(bp.PORT_4)))
        countdown = 50
    return countdown - 1

if __name__ == "__main__":
    running = True

    bp = Control_BrickPi.initialize_brickpi_sensors()
    Keyboard_Input.initialize_pygame()

    key_states = Keyboard_Input.initialize_keyboard_inputs()
    countdown = 50

    while running:

        # check mode input van keyboard
        key_states, running = Keyboard_Input.get_keyboard_input(key_states, running, bp)

        if key_states["mode"] == 0:
            Manual_Driving.manual_driving(bp, key_states)
            countdown = print_sensors(bp,countdown)
        elif key_states["mode"] == 1:
            Self_Driving_Naive.self_driving(bp)
        elif key_states["mode"] == 2:
            Self_Driving_Follow_Right_Wall.self_driving(bp)
        elif key_states["mode"] == 3:
            Smooth_Operator.self_driving(bp)

        time.sleep(0.02)
    