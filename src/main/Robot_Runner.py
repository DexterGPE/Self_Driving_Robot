import time

import Self_Driving_Naive
import Self_Driving_Follow_Right_Wall
import Manual_Driving
import Keyboard_Input
import Control_BrickPi

# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15

if __name__ == "__main__":
    running = True

    BP = Control_BrickPi.initialize_brickpi_sensors()
    Keyboard_Input.initialize_pygame()

    key_states = Keyboard_Input.initialize_keyboard_inputs()

    while running:

        # check mode input van keyboard
        key_states, running = Keyboard_Input.get_keyboard_input(key_states, running, BP)

        if key_states["mode"] == 0:
            Manual_Driving.manual_driving(BP, key_states)
        elif key_states["mode"] == 1:
            Self_Driving_Naive.self_driving(BP)
        elif key_states["mode"] == 2:
            Self_Driving_Follow_Right_Wall.self_driving(BP)

        time.sleep(0.02)
