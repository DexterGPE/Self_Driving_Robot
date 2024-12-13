import Self_Driving_Naive
import Control_BrickPi

import time


# smoothness = 5
# bridgesmoothness = 10
# standard_speed = -30
# turn_speed = 10
# distance_to_wall = 15


def self_driving(bp, speed_left, speed_right, wall_finding, time_since_black_line, smoothness, bridgesmoothness,
                 standard_speed, turn_speed, distance_to_wall):
    pars = {
        "smoothness": smoothness,
        "bridgesmoothness": bridgesmoothness,
        "standard_speed": standard_speed,
        "turn_speed": turn_speed,
        "distance_to_wall": distance_to_wall
    }
    # wall_finding -= 1 # Probably obsolete
    time_since_black_line -= 1
    try:
        if detect_black(bp):
            time_since_black_line = 100
        if Self_Driving_Naive.bumped_into_wall(bp):
            if detect_finish(bp, distance_to_wall):
                speed_left = 0
                speed_right = 0
            else:
                turn_left_after_bump(bp)
                speed_left = 0
                speed_right = 0
        elif red_line_found(bp) and time_since_black_line > 0:
            Control_BrickPi.set_motor_power(bp, pars["standard_speed"], pars["standard_speed"])
        elif red_line_found(bp):
            wall_finding = 25
            speed_left, speed_right = smooth_left_turn_on_bridge(speed_left, speed_right, pars)
        elif get_right_wall_distance(bp) > 33:
            speed_left, speed_right = smooth_right_turn_on_bridge(speed_left, speed_right, pars)
        else:
            speed_left, speed_right = smooth_turn_at_wall(bp, pars)
    except:
        print("Invalid sensor data.")

    Control_BrickPi.set_motor_power(bp, int(speed_left), int(speed_right))

    return speed_left, speed_right, wall_finding, time_since_black_line


def turn_left_after_bump(bp):
    time.sleep(0.4)  # drive into wall to set it straight
    Self_Driving_Naive.reverse_after_bump(bp)
    speed_left, speed_right = turn_left()
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.65)


def is_right_wall_found(bp, distance_to_wall):
    return bp.get_sensor(bp.PORT_1) < distance_to_wall

def get_right_wall_distance(bp):
    return bp.get_sensor(bp.PORT_1)


def smooth_turn_at_wall(bp, pars):
    distance = get_right_wall_distance(bp)
    correction_factor = max(-1, min(1, (distance - pars["distance_to_wall"]) / pars["smoothness"]))
    speed_left = pars["standard_speed"] - pars["turn_speed"] * correction_factor
    speed_right = pars["standard_speed"] + pars["turn_speed"] * correction_factor
    return speed_left, speed_right


def smooth_left_turn_on_bridge(speed_left, speed_right, pars):
    speed_left = max(pars["standard_speed"] + pars["turn_speed"],
                     speed_left + pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"]))
    speed_left = max(speed_left, "standard_speed")
    speed_right = max(pars["standard_speed"] - pars["turn_speed"],
                      speed_right - pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"]))
    speed_right = max(speed_right, "standard_speed")
    return speed_left, speed_right


def smooth_right_turn_on_bridge(speed_left, speed_right, pars):
    speed_left = max(pars["standard_speed"] - pars["turn_speed"],
                     speed_left - pars["sturn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"]))
    speed_left = max(speed_left, "standard_speed")
    speed_right = max(pars["standard_speed"] + pars["turn_speed"],
                      speed_right + pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"]))
    speed_right = max(speed_right, "standard_speed")
    return speed_left, speed_right


def red_line_found(bp):
    return (bp.get_sensor(bp.PORT_4)[0] > 130) and (bp.get_sensor(bp.PORT_4)[1] < 40) and (
            bp.get_sensor(bp.PORT_4)[2] < 40)


def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right


def turn_right():
    speed_left = -30
    speed_right = 30
    return speed_left, speed_right


def detect_black(bp):
    return (bp.get_sensor(bp.PORT_4)[0] < 45) and (bp.get_sensor(bp.PORT_4)[1] < 45) and (
            bp.get_sensor(bp.PORT_4)[2] < 45)


def detect_finish(bp, distance_to_wall):
    return detect_black(bp) and is_right_wall_found(bp, distance_to_wall)
