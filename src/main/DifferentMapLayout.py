from SmoothOperator import SmoothOperator
import Control_BrickPi
import time


class DifferentMapLayout(SmoothOperator):
    @classmethod
    def turn_left_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_left(pars)
        Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1 * -30 / pars["standard_speed"])

    @classmethod
    def turn_right_after_bump(cls, bp, pars):
        cls.reverse_after_bump(bp, pars)
        speed_left, speed_right = cls.turn_right(pars)
        Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
        time.sleep(1 * -30 / pars["standard_speed"])