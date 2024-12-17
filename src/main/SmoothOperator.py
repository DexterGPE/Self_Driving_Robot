import Control_BrickPi
import time

class SmoothOperator:

    @classmethod
    def self_driving(cls, bp, speed_left, speed_right, pars):
        blade_speed = 50

        try:
            if cls.bumped_into_wall(bp):
                if cls.detect_finish(bp, pars["distance_to_wall"]):
                    pars["mode"] = 0
                else:
                    speed_left, speed_right = cls.turn_after_bump(bp, pars)

            elif cls.red_line_found(bp) and cls.get_right_wall_distance(bp) > 23:
                speed_left, speed_right = cls.smooth_left_turn_on_bridge(speed_left, speed_right, pars)
            elif cls.get_right_wall_distance(bp) > 23:
                speed_left, speed_right = cls.smooth_right_turn_on_bridge(speed_left, speed_right, pars)
            else:
                speed_left, speed_right = cls.smooth_turn_at_wall(bp, pars)

        except:
            print("Invalid sensor data.")

        Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
        Control_BrickPi.set_blade_power(bp, blade_speed)

        return speed_left, speed_right, pars["mode"]

    @classmethod
    def turn_after_bump(cls, bp, pars):
        if cls.is_right_wall_found(bp, pars["distance_to_wall"]):
            cls.turn_left_after_bump(bp, pars)
        else:
            cls.turn_right_after_bump(bp, pars)
        return 0, 0

    @classmethod
    def turn_left_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_left(pars)
        Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1.55 * -30 / pars["standard_speed"])

    @classmethod
    def turn_right_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_right(pars)
        Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1.55 * -30 / pars["standard_speed"])

    @staticmethod
    def is_right_wall_found(bp, distance_to_wall):
        return bp.get_sensor(bp.PORT_1) < 30

    @staticmethod
    def get_right_wall_distance(bp):
        return bp.get_sensor(bp.PORT_1)

    @classmethod
    def smooth_turn_at_wall(cls, bp, pars):
        distance = cls.get_right_wall_distance(bp)
        correction_factor = max(-1, min(1, (distance - pars["distance_to_wall"]) / pars["smoothness"]))
        speed_left = pars["standard_speed"] + pars["turn_speed"] * correction_factor
        speed_right = pars["standard_speed"] - pars["turn_speed"] * correction_factor
        return speed_left, speed_right

    @staticmethod
    def smooth_left_turn_on_bridge(speed_left, speed_right, pars):
        speed_left = min(pars["standard_speed"] - pars["turn_speed"],
                         speed_left - (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"])

        speed_right = max(pars["standard_speed"] + pars["turn_speed"],
                          speed_right + (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"])

        return speed_left, speed_right

    @staticmethod
    def smooth_right_turn_on_bridge(speed_left, speed_right, pars):
        speed_left = max(pars["standard_speed"] + pars["turn_speed"],
                         speed_left + (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"])

        speed_right = min(pars["standard_speed"] - pars["turn_speed"],
                          speed_right - (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"])

        return speed_left, speed_right

    @staticmethod
    def red_line_found(bp):
        return bp.get_sensor(bp.PORT_4)[0] > 1.7 * bp.get_sensor(bp.PORT_4)[1] and bp.get_sensor(bp.PORT_4)[0] > 2.5 * \
            bp.get_sensor(bp.PORT_4)[2]

    @staticmethod
    def turn_left(pars):
        speed_left = -pars["standard_speed"]
        speed_right = pars["standard_speed"]
        return speed_left, speed_right

    @staticmethod
    def turn_right(pars):
        speed_left = pars["standard_speed"]
        speed_right = -pars["standard_speed"]
        return speed_left, speed_right

    @staticmethod
    def detect_black(bp):
        return (bp.get_sensor(bp.PORT_4)[0] < 35) and (bp.get_sensor(bp.PORT_4)[1] < 45) and (
                bp.get_sensor(bp.PORT_4)[2] < 25)

    @classmethod
    def detect_finish(cls, bp, distance_to_wall):
        return cls.detect_black(bp) and cls.is_right_wall_found(bp, distance_to_wall)

    @staticmethod
    def bumped_into_wall(bp):
        return bp.get_sensor(bp.PORT_2) or bp.get_sensor(bp.PORT_3)

    @staticmethod
    def reverse_after_bump(bp, pars):
        speed_left = -pars["standard_speed"]
        speed_right = -pars["standard_speed"]
        Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(0.40 * -30 / pars["standard_speed"])
