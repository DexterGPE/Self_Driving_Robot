import Self_Driving_Naive
import Control_BrickPi
import Smooth_Operator

import time


def self_driving(bp, speed_left, speed_right, wall_finding, time_since_red_line, smoothness, bridgesmoothness,
                 standard_speed, turn_speed, distance_to_wall, mode):
    pars = {
        "smoothness": smoothness,
        "bridgesmoothness": bridgesmoothness,
        "standard_speed": standard_speed,
        "turn_speed": turn_speed,
        "distance_to_wall": distance_to_wall
    }
    wall_finding -= 1 # Probably obsolete
    time_since_red_line -= 1
    blade_speed = 50
    try:
        if Self_Driving_Naive.bumped_into_wall(bp):
            print("bumped into wall")
            if Smooth_Operator.detect_finish(bp, distance_to_wall):
                print("Bumped into wall and detected finish")
                speed_left = 0
                speed_right = 0
                mode = 0
            else:
                print("Bumped into wall, no finish detected")
                if Smooth_Operator.is_right_wall_found(bp, distance_to_wall):
                    Smooth_Operator.turn_left_after_bump(bp, pars)
                else:
                    Smooth_Operator.turn_right_after_bump(bp, pars)

                speed_left = 0
                speed_right = 0
        elif Smooth_Operator.red_line_found(bp) and Smooth_Operator.get_right_wall_distance(bp) > 23:
            print("Found red line")
            wall_finding = 25
            time_since_red_line = 50
            speed_left, speed_right = smooth_left_turn_on_bridge(pars)
        elif Smooth_Operator.get_right_wall_distance(bp) > 23:
            print("No right wall found (should happen on bridge only)")
            speed_left, speed_right = smooth_right_turn_on_bridge(pars)
        elif wall_finding < 0:
            print("else: smooth turn at wall")
            speed_left, speed_right = Smooth_Operator.smooth_turn_at_wall(bp, pars)
    except:
        print("Invalid sensor data.")
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    Control_BrickPi.set_blade_power(bp, blade_speed)

    return speed_left, speed_right, wall_finding, time_since_red_line, mode

def smooth_left_turn_on_bridge(pars):
    speed_left = pars["standard_speed"] - pars["turn_speed"]
    speed_right = pars["standard_speed"] + pars["turn_speed"]
    return speed_left/2.5, speed_right/2.5


def smooth_right_turn_on_bridge(pars):
    speed_left = pars["standard_speed"] + pars["turn_speed"]
    speed_right = pars["standard_speed"] - pars["turn_speed"]
    return speed_left/2.5, speed_right/2.5