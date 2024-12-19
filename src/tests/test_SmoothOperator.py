import unittest
from unittest.mock import MagicMock, patch
import sys


sys.path.append('../main')
sys.path.append('./main')
sys.path.append('..')
sys.path.append('./src/main')

# Mock the brickpi3 module
with patch.dict('sys.modules', {'brickpi3': MagicMock()}):
    import brickpi3
    from main.SmoothOperator import SmoothOperator
    from main.ControlBrickPi import get_red, get_green, get_blue


class TestSmoothOperator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock BrickPi3 and its methods
        brickpi3.BrickPi3.return_value = MagicMock()
        cls.bp = brickpi3.BrickPi3()

        # Mock ControlBrickPi methods
        cls.mock_get_red = MagicMock()
        cls.mock_get_green = MagicMock()
        cls.mock_get_blue = MagicMock()
        get_red = cls.mock_get_red
        get_green = cls.mock_get_green
        get_blue = cls.mock_get_blue


    def test_right_wall_is_found(self):
        self.bp.get_sensor.return_value = 15

        result = SmoothOperator.is_right_wall_found(self.bp, 30)

        self.assertTrue(result)

    def test_right_wall_is_not_found(self):
        self.bp.get_sensor.return_value = 45

        result = SmoothOperator.is_right_wall_found(self.bp, 30)

        self.assertFalse(result)

    def test_get_right_wall_distance(self):
        self.bp.get_sensor.return_value = 30

        result = SmoothOperator.get_right_wall_distance(self.bp)

        self.assertEqual(30, result)

    def test_high_speed_correction_left_speed_over_100(self):
        speed_left, speed_right = -160, 100

        speed_left_result, speed_right_result = SmoothOperator.high_speed_correction(
            speed_left, speed_right)

        self.assertEqual(-100, speed_left_result)
        self.assertEqual(62.5, speed_right_result)

    def test_high_speed_correction_right_speed_over_100(self):
        speed_left, speed_right = -100, -160

        speed_left_result, speed_right_result = SmoothOperator.high_speed_correction(
            speed_left, speed_right)

        self.assertEqual(-62.5, speed_left_result)
        self.assertEqual(-100, speed_right_result)

    def test_smooth_left_turn_on_bridge(self):
        speed_left, speed_right = -30, -30
        pars = {"standard_speed": -30, "turn_speed": -15,
                "smoothness": 5, "bridgesmoothness":2}

        speed_left, speed_right = SmoothOperator.smooth_left_turn_on_bridge(
             speed_left, speed_right, pars)

        self.assertEqual(-28.5, speed_left)
        self.assertEqual(-31.5, speed_right)

    def test_smooth_right_turn_on_bridge(self):
        speed_left, speed_right = -30, -30
        pars = {"standard_speed": -30, "turn_speed": -15,
                "smoothness": 5, "bridgesmoothness":2}

        speed_left, speed_right = SmoothOperator.smooth_right_turn_on_bridge(
             speed_left, speed_right, pars)

        self.assertEqual(-31.5, speed_left)
        self.assertEqual(-28.5, speed_right)

    def test_red_line_not_found_same_for_rgb(self):

        self.bp.get_sensor.return_value = (30,30,30)

        result = SmoothOperator.red_line_found(self.bp)

        self.assertFalse(result)

    def test_red_line_not_found_different_rgb_but_not_red(self):

        self.bp.get_sensor.return_value = (45,30,60)

        result = SmoothOperator.red_line_found(self.bp)

        self.assertFalse(result)

    def test_red_line_found(self):
        self.bp.get_sensor.return_value = (100, 0, 0)

        result = SmoothOperator.red_line_found(self.bp)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
