from SmoothOperator import SmoothOperator

class  SportMode(SmoothOperator):

    @staticmethod
    def smooth_left_turn_on_bridge(_, __, pars):
        speed_left = pars["standard_speed"] - pars["turn_speed"]
        speed_right = pars["standard_speed"] + pars["turn_speed"]
        return speed_left, speed_right

    @staticmethod
    def smooth_right_turn_on_bridge(_, __, pars):
        speed_left = pars["standard_speed"] + pars["turn_speed"]
        speed_right = pars["standard_speed"] - pars["turn_speed"]
        return speed_left, speed_right
