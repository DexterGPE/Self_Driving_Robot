from SmoothOperator import SmoothOperator


class SportMode(SmoothOperator):

    @classmethod
    def smooth_left_turn_on_bridge(cls, _, __, pars):
        speed_left = pars["standard_speed"] - pars["turn_speed"]
        speed_right = pars["standard_speed"] + pars["turn_speed"]
        speed_left, speed_right = cls.high_speed_correction(
            speed_left, speed_right)
        return speed_left, speed_right

    @classmethod
    def smooth_right_turn_on_bridge(cls, _, __, pars):
        speed_left = pars["standard_speed"] + pars["turn_speed"]
        speed_right = pars["standard_speed"] - pars["turn_speed"]
        speed_left, speed_right = cls.high_speed_correction(
            speed_left, speed_right)
        return speed_left, speed_right
