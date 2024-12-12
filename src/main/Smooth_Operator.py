import Self_Driving_Naive
import Control_BrickPi

import time

# smoothness = 5
# bridgesmoothness = 10
# standard_speed = -30
# turn_speed = 10
# distance_to_wall = 15


def self_driving(bp, speed_left, speed_right, smoothness, bridgesmoothness, standard_speed, turn_speed, distance_to_wall):
    pars = {
        "smoothness" : smoothness,
        "bridgesmoothness" : bridgesmoothness,
        "standard_speed" : standard_speed,
        "turn_speed" : turn_speed, 
        "distance_to_wall" : distance_to_wall
    }
    if Self_Driving_Naive.bumped_into_wall(bp):
        if detect_finish(bp):
            speed_left = 0
            speed_right = 0
        else:
            turn_left_after_bump(bp)
            speed_left = 0
            speed_right = 0
    elif red_line_found(bp):
        speed_left, speed_right = smooth_left_turn_on_bridge(speed_left, speed_right, pars)
    elif get_right_wall_distance(bp) > 80:
        speed_left, speed_right = smooth_right_turn_on_bridge(speed_left, speed_right, pars)
    else:
        speed_left, speed_right = smooth_turn_at_wall(bp, pars)
    
    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)

    return speed_left, speed_right

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
    correction_factor = max(-1, min(1, (distance-pars["distance_to_wall"])/pars["smoothness"]))
    speed_left = pars["standard_speed"] - pars["turn_speed"] * correction_factor
    speed_right = pars["standard_speed"] + pars["turn_speed"] * correction_factor
    return speed_left, speed_right

def smooth_left_turn_on_bridge(speed_left, speed_right, pars):
    speed_left = max(pars["standard_speed"] + pars["turn_speed"], pars["speed_left"] + pars["turn_speed"]/(pars["bridgesmoothness"]*pars["smoothness"]))
    speed_right = max(pars["standard_speed"] - pars["turn_speed"], pars["speed_right"] - pars["turn_speed"]/(pars["bridgesmoothness"]*pars["smoothness"]))
    return speed_left, speed_right

def smooth_right_turn_on_bridge(speed_left, speed_right, pars):
    speed_left = max(pars["standard_speed"] - pars["turn_speed"], pars["speed_left"] - parameter["sturn_speed"]/(pars["bridgesmoothness"]*pars["smoothness"]))
    speed_right = max(pars["standard_speed"] + pars["turn_speed"], pars["speed_right"] + pars["turn_speed"]/(pars["bridgesmoothness"]*pars["smoothness"]))
    return speed_left, speed_right

def red_line_found(bp):
    print("Red line found!")
    return (bp.get_sensor(bp.PORT_4)[0] > 15) and (bp.get_sensor(bp.PORT_4)[1] < 5) and (
            bp.get_sensor(bp.PORT_4)[2] < 5)

def turn_left():
    speed_left = 30
    speed_right = -30
    return speed_left, speed_right

def turn_right():
    speed_left = -30
    speed_right = 30
    return speed_left, speed_right

def detect_black(bp):
    return (bp.get_sensor(bp.PORT_4)[0] < 5) and (bp.get_sensor(bp.PORT_4)[1] < 5) and (
            bp.get_sensor(bp.PORT_4)[2] < 5)

def detect_finish(bp):
    return detect_black(bp) and is_right_wall_found(bp)
