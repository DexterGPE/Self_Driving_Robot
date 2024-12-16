import Self_Driving_Naive
import Control_BrickPi

import time


# smoothness = 5
# bridgesmoothness = 10
# standard_speed = -30
# turn_speed = 10
# distance_to_wall = 15





def self_driving(bp, speed_left, speed_right, wall_finding, time_since_black_line, smoothness, bridgesmoothness,
                 standard_speed, turn_speed, distance_to_wall, mode):
    pars = {
        "smoothness": smoothness,
        "bridgesmoothness": bridgesmoothness,
        "standard_speed": standard_speed,
        "turn_speed": turn_speed,
        "distance_to_wall": distance_to_wall
    }
    wall_finding -= 1 # Probably obsolete
    time_since_black_line -= 1
    blade_speed = 50

    try:
        if detect_black(bp):
            print("detected black surface")
            time_since_black_line = 50
        if Self_Driving_Naive.bumped_into_wall(bp):
            print("bumped into wall")
            if detect_finish(bp, distance_to_wall):
                print("Bumped into wall and detected finish")
                speed_left = 0
                speed_right = 0
                mode = 0
            else:
                print("Bumped into wall, no finish detected")
                if is_right_wall_found(bp, distance_to_wall):
                    turn_left_after_bump(bp,pars)
                else:
                    turn_right_after_bump(bp,pars)

                speed_left = 0
                speed_right = 0
        elif red_line_found(bp) and get_right_wall_distance(bp) > 23:
            print("Found red line")
            wall_finding = 25
            speed_left, speed_right = smooth_left_turn_on_bridge(speed_left, speed_right, pars)
        elif get_right_wall_distance(bp) > 23:
            print("No right wall found and no red line found (should happen on bridge only)")
            speed_left, speed_right = smooth_right_turn_on_bridge(speed_left, speed_right, pars)
        elif wall_finding < 0:
            print("else: smooth turn at wall")
            speed_left, speed_right = smooth_turn_at_wall(bp, pars)

    except:
        print("Invalid sensor data.")
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    Control_BrickPi.set_blade_power(bp, blade_speed)

    return speed_left, speed_right, wall_finding, time_since_black_line, mode


def turn_left_after_bump(bp,pars):
    Self_Driving_Naive.reverse_after_bump(bp,pars)
    speed_left, speed_right = turn_left(pars)
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.55*-30/pars["standard_speed"])

def turn_right_after_bump(bp,pars):
    Self_Driving_Naive.reverse_after_bump(bp,pars)
    speed_left, speed_right = turn_right(pars)
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    time.sleep(1.55*-30/pars["standard_speed"])


def is_right_wall_found(bp, distance_to_wall):
    return bp.get_sensor(bp.PORT_1) < 30


def get_right_wall_distance(bp):
    return bp.get_sensor(bp.PORT_1)


def smooth_turn_at_wall(bp, pars):
    distance = get_right_wall_distance(bp)
    correction_factor = max(-1, min(1, (distance - pars["distance_to_wall"]) / pars["smoothness"]))
    speed_left = pars["standard_speed"] + pars["turn_speed"] * correction_factor
    speed_right = pars["standard_speed"] - pars["turn_speed"] * correction_factor
    return speed_left, speed_right


def smooth_left_turn_on_bridge(speed_left, speed_right, pars):
    speed_left = min(pars["standard_speed"] - pars["turn_speed"],
                     speed_left - (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))

    speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"])


    speed_right = max(pars["standard_speed"] + pars["turn_speed"],
                      speed_right + (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))

    speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"])

     # speed_left = pars["standard_speed"] - pars["turn_speed"]
    # speed_right = pars["standard_speed"] + pars["turn_speed"]
    return speed_left, speed_right

def smooth_right_turn_on_bridge(speed_left, speed_right, pars):
    speed_left = max(pars["standard_speed"] + pars["turn_speed"],
                     speed_left + (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
    speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"])
    speed_right = min(pars["standard_speed"] - pars["turn_speed"],
                      speed_right - (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
    speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"])
    # speed_left = pars["standard_speed"] + pars["turn_speed"]
    # speed_right = pars["standard_speed"] - pars["turn_speed"]
    return speed_left, speed_right


def red_line_found(bp):
    # 0 is 1.7x zo hoog als b en g
    return bp.get_sensor(bp.PORT_4)[0] > 1.7 * bp.get_sensor(bp.PORT_4)[1] and bp.get_sensor(bp.PORT_4)[0] > 2.5 * bp.get_sensor(bp.PORT_4)[2]
    # return (bp.get_sensor(bp.PORT_4)[0] > 120) and (bp.get_sensor(bp.PORT_4)[1] < 40) and (
    #         bp.get_sensor(bp.PORT_4)[2] < 20)


def turn_left(pars):
    speed_left = -pars["standard_speed"]
    speed_right = pars["standard_speed"]
    return speed_left, speed_right


def turn_right(pars):
    speed_left = pars["standard_speed"]
    speed_right = -pars["standard_speed"]
    return speed_left, speed_right


def detect_black(bp):
    return (bp.get_sensor(bp.PORT_4)[0] < 35) and (bp.get_sensor(bp.PORT_4)[1] < 45) and (
            bp.get_sensor(bp.PORT_4)[2] < 25)


def detect_finish(bp, distance_to_wall):
    return detect_black(bp) and is_right_wall_found(bp, distance_to_wall)
