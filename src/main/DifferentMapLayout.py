from SmoothOperator import SmoothOperator
import ControlBrickPi
import time


class DifferentMapLayout(SmoothOperator):
    @classmethod
    def turn_left_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_left(pars)
        ControlBrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1 * -30 / pars["standard_speed"])

    @classmethod
    def turn_right_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_right(pars)
        ControlBrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1 * -30 / pars["standard_speed"])

    @classmethod
    def smooth_left_turn_on_bridge(cls, speed_left, speed_right, pars):
        speed_left = min(pars["standard_speed"] - pars["turn_speed"] / 2,
                         speed_left - (pars["turn_speed"] /
                                       (pars["bridgesmoothness"] * pars["smoothness"])))
        speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"] / 2)

        speed_right = max(pars["standard_speed"] + pars["turn_speed"] / 2,
                          speed_right + (pars["turn_speed"] /
                                         (pars["bridgesmoothness"] * pars[
                                             "smoothness"])))
        speed_right = min(speed_right, pars["standard_speed"] - pars["turn_speed"] / 2)

        return speed_left, speed_right

    @classmethod
    def smooth_right_turn_on_bridge(cls, speed_left, speed_right, pars):
        speed_left = max(
            pars["standard_speed"] + pars["turn_speed"] * pars["turn_factor"],
            speed_left + (pars["turn_speed"] / (
                    pars["bridgesmoothness"] * pars["smoothness"])))
        speed_left = min(speed_left, pars["standard_speed"] - pars["turn_speed"] * pars[
            "turn_factor"])

        speed_right = min(
            pars["standard_speed"] - pars["turn_speed"] * pars["turn_factor"],
            speed_right - (pars["turn_speed"] / (
                    pars["bridgesmoothness"] * pars["smoothness"])))
        speed_right = min(speed_right,
                          pars["standard_speed"] - pars["turn_speed"] * pars[
                              "turn_factor"])

        return speed_left, speed_right
