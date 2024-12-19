import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append('../main')

# Mock the brickpi3 module
with patch.dict('sys.modules', {'brickpi3': MagicMock()}):
    # import brickpi3
    from main.SportMode import SportMode
    from main.SmoothOperator import SmoothOperator


class TestSportMode(unittest.TestCase):
    def test_smooth_left_turn_on_bridge_without_correction(self):
        pars = {"standard_speed": -50,
                "turn_speed": -25}
        speed_left, speed_right =0, 0
        resulting_speed_left, resulting_speed_right = SportMode.smooth_left_turn_on_bridge(speed_left, speed_right, pars)

        self.assertEqual(-25 ,resulting_speed_left)
        self.assertEqual(-75, resulting_speed_right)

    def test_smooth_left_turn_on_bridge_with_correction(self):
        pars = {"standard_speed": -80,
                "turn_speed": -40}
        speed_left, speed_right =0, 0
        resulting_speed_left, resulting_speed_right = SportMode.smooth_left_turn_on_bridge(speed_left, speed_right, pars)

        self.assertAlmostEqual(-33.33 ,resulting_speed_left, delta=0.01)
        self.assertEqual(-100, resulting_speed_right)

    def test_smooth_right_turn_on_bridge_without_correction(self):
        pars = {"standard_speed": -50,
                "turn_speed": -25}
        speed_left, speed_right =0, 0
        resulting_speed_left, resulting_speed_right = SportMode.smooth_left_turn_on_bridge(speed_left, speed_right, pars)

        self.assertEqual(-75, resulting_speed_left)
        self.assertEqual(-25, resulting_speed_right)

    def test_smooth_right_turn_on_bridge_with_correction(self):
        pars = {"standard_speed": -80,
                "turn_speed": -40}
        speed_left, speed_right =0, 0
        resulting_speed_left, resulting_speed_right = SportMode.smooth_left_turn_on_bridge(speed_left, speed_right, pars)

        self.assertAlmostEqual(-33.33 ,resulting_speed_right, delta=0.01)
        self.assertEqual(-100, resulting_speed_left)


if __name__ == '__main__':
    unittest.main()
