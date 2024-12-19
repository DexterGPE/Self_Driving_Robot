import ControlBrickPi
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

        ControlBrickPi.set_motor_power(bp, speed_left, speed_right)
        ControlBrickPi.set_blade_power(bp, blade_speed)

        return speed_left, speed_right, pars

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
        ControlBrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1.55 * -30 / pars["standard_speed"])

    @classmethod
    def turn_right_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_right(pars)
        ControlBrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1.55 * -30 / pars["standard_speed"])

    @staticmethod
    def is_right_wall_found(bp, distance_to_wall):
        return ControlBrickPi.get_distance(bp) < 30

    @staticmethod
    def get_right_wall_distance(bp):
        return ControlBrickPi.get_distance(bp)

    @classmethod
    def smooth_turn_at_wall(cls, bp, pars):
        distance = cls.get_right_wall_distance(bp)
        correction_factor = max(-1, min(1, (distance - pars["distance_to_wall"]) / pars["smoothness"]))
        speed_left = pars["standard_speed"] + pars["turn_speed"] * correction_factor
        speed_right = pars["standard_speed"] - pars["turn_speed"] * correction_factor
        speed_left, speed_right = cls.high_speed_correction(speed_left, speed_right)
        return speed_left, speed_right

    @staticmethod
    def high_speed_correction(speed_left, speed_right):
        factor = 1
        if speed_left < -100:
            factor = speed_left / -100

        elif speed_right < -100:
            factor = speed_right / -100
        return speed_left / factor, speed_right / factor

    @classmethod
    def smooth_left_turn_on_bridge(cls, speed_left, speed_right, pars):
        speed_left = min(pars["standard_speed"] - pars["turn_speed"],
                         speed_left - (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"])

        speed_right = max(pars["standard_speed"] + pars["turn_speed"],
                          speed_right + (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"])
        speed_left, speed_right = cls.high_speed_correction(speed_left, speed_right)
        return speed_left, speed_right

    @classmethod
    def smooth_right_turn_on_bridge(cls, speed_left, speed_right, pars):
        speed_left = max(pars["standard_speed"] + pars["turn_speed"],
                         speed_left + (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"])

        speed_right = min(pars["standard_speed"] - pars["turn_speed"],
                          speed_right - (pars["turn_speed"] / (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"])
        speed_left, speed_right = cls.high_speed_correction(speed_left, speed_right)
        return speed_left, speed_right

    @staticmethod
    def red_line_found(bp):
        return ControlBrickPi.get_red(bp) > 1.7 * ControlBrickPi.get_green(bp) and ControlBrickPi.get_red(bp) > 2.5 * \
            ControlBrickPi.get_blue(bp)

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
        return (ControlBrickPi.get_red(bp) < 35) and (ControlBrickPi.get_green(bp) < 45) and (
                ControlBrickPi.get_blue(bp) < 25)

    @classmethod
    def detect_finish(cls, bp, distance_to_wall):
        return cls.detect_black(bp) and cls.is_right_wall_found(bp, distance_to_wall)

    @staticmethod
    def bumped_into_wall(bp):
        return ControlBrickPi.get_right_bumper(bp) or ControlBrickPi.get_left_bumper(bp)

    @staticmethod
    def reverse_after_bump(bp, pars):
        speed_left = -pars["standard_speed"]
        speed_right = -pars["standard_speed"]
        ControlBrickPi.set_motor_power(bp, speed_left, speed_right)
        if not pars["super_speed"]:
            time.sleep(0.40 * -30 / pars["standard_speed"])
