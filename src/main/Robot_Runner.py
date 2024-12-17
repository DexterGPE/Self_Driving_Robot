import time

import Manual_Driving
import Keyboard_Input
import Control_BrickPi
from Smooth_Operator import Smooth_Operator
from Sport_Mode import Sport_Mode
import finish_celebration_1


def print_sensors(bp, countdown):
    try:
        if countdown == 0:
            print("Wall distance: {0}".format(bp.get_sensor(bp.PORT_1)))
            print("Color: {0}".format(bp.get_sensor(bp.PORT_4)))
            print("Left touch pushed: {0}".format(bp.get_sensor(bp.PORT_3)))
            print("Right touch pushed: {0}".format(bp.get_sensor(bp.PORT_2)))
            countdown = 50
    except:
        print("Invalid sensor data")
    return countdown - 1


if __name__ == "__main__":
    running = True

    bp = Control_BrickPi.initialize_brickpi_sensors()
    Keyboard_Input.initialize_pygame()

    key_states = Keyboard_Input.initialize_keyboard_inputs()
    print_countdown = 50
    speed_left = 0
    speed_right = 0
    wall_finding = 25

    while running:
        # check mode input van keyboard
        key_states, running = Keyboard_Input.get_keyboard_input(key_states, running, bp)

        # Start mode
        if key_states["mode"] == 0:
            Manual_Driving.manual_driving(bp, key_states)
            print_countdown = print_sensors(bp, print_countdown)

        elif key_states["mode"] == 1:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2,
                "standard_speed": -30,
                "turn_speed": -15,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            # Slow smooth mode
            speed_left, speed_right, key_states["mode"] = Smooth_Operator.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 2: # Fast sport mode
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2.2,
                "standard_speed": -60,
                "turn_speed": -30,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Sport_Mode.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 3:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2,
                "standard_speed": -30,
                "turn_speed": -15,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Smooth_Operator.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 4: # Finish celebration mode
            key_states["mode"] = "finish1"

        elif key_states["mode"] == 5:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2.2,
                "standard_speed": -60,
                "turn_speed": -30,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Sport_Mode.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 6:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2.3,
                "standard_speed": -70,
                "turn_speed": -35,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Smooth_Operator.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 7:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2.4,
                "standard_speed": -80,
                "turn_speed": -40,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Smooth_Operator.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 8:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2.5,
                "standard_speed": -30,
                "turn_speed": -15,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Smooth_Operator.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == 9:
            pars = {
                "smoothness": 5,
                "bridgesmoothness": 2.2,
                "standard_speed": -60,
                "turn_speed": -30,
                "distance_to_wall": 18,
                "mode" : key_states["mode"]
            }
            speed_left, speed_right, key_states["mode"] = Smooth_Operator.self_driving(bp, speed_left, speed_right, pars)

        elif key_states["mode"] == "finish1":
            finish_celebration_1.celebration_1(bp)

        time.sleep(0.02) # Short sleep time so the raspberrypi is not overloaded
