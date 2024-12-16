import time

import Manual_Driving
import Keyboard_Input
import Control_BrickPi
import Smooth_Operator
import sport_mode
from src.main.finish_celebration_1 import celebration_1


# zwart op bord: alles onder de 15
# grijs op bord: R en G rond de 30, B 15
# Rood op bord: R 40-50, andere onder de 15


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
    countdown = 50
    speed_left = 0
    speed_right = 0
    wall_finding = 25
    time_since_red_line = 0

    while running:
        # check mode input van keyboard
        key_states, running = Keyboard_Input.get_keyboard_input(key_states, running, bp)

        if key_states["mode"] == 0:
            Manual_Driving.manual_driving(bp, key_states)
            # countdown = print_sensors(bp,countdown)
        elif key_states["mode"] == 1:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp, speed_left, speed_right, wall_finding, time_since_red_line, 5, 2, -30, -15, 18, key_states["mode"])
        elif key_states["mode"] == 2:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = sport_mode.self_driving(
                bp, speed_left, speed_right, wall_finding, time_since_red_line, 5, 2.2, -60, -30, 18,key_states["mode"])
        elif key_states["mode"] == 3:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_red_line, 5, 2, -30, 15, 18, key_states["mode"])
        elif key_states["mode"] == 4:
            key_states["mode"] = "finish1"
        elif key_states["mode"] == 5:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = sport_mode.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_red_line, 5, 2.2, -60, 30, 18, key_states["mode"])
        elif key_states["mode"] == 6:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_red_line, 5, 2.3, -70, 35, 18, key_states["mode"])
        elif key_states["mode"] == 7:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_red_line, 5, 2.4, -80, 40, 18, key_states["mode"])
        elif key_states["mode"] == 8:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_red_line, 5, 2.5, -30, 15, 18, key_states["mode"])
        elif key_states["mode"] == 9:
            speed_left, speed_right, wall_finding, time_since_red_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_red_line, 5, 2.2, -60, -30, 18, key_states["mode"])
        elif key_states["mode"] == "finish1":
            celebration_1(bp)


        time.sleep(0.02)
    