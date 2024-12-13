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
    time_since_black_line = 0

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
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2, -30, 15, 15, key_states["mode"])
        elif key_states["mode"] == 4:
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2.1, -30, 15, 17, key_states["mode"])
        elif key_states["mode"] == 5:
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2.2, -30, 16, 17, key_states["mode"])
        elif key_states["mode"] == 6:
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2.3, -30, 17, 17, key_states["mode"])
        elif key_states["mode"] == 7:
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2.4, -30, 15, 18, key_states["mode"])
        elif key_states["mode"] == 8:
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2.5, -30, 16, 18, key_states["mode"])
        elif key_states["mode"] == 9:
            speed_left, speed_right, wall_finding, time_since_black_line, key_states["mode"] = Smooth_Operator.self_driving(
                bp,speed_left, speed_right, wall_finding, time_since_black_line, 5, 2.6, -30, 17, 18, key_states["mode"])
        time.sleep(0.02)
    