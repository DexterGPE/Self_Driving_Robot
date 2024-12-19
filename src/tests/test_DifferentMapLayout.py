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
    from main.DifferentMapLayout import DifferentMapLayout
    from main.SmoothOperator import SmoothOperator


class TestDifferentMapLayout(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock BrickPi3 and its methods
        brickpi3.BrickPi3.return_value = MagicMock()
        cls.bp = brickpi3.BrickPi3()

        # Mock ports and sensor types
        cls.bp.PORT_A = "PORT_A"
        cls.bp.PORT_B = "PORT_B"
        cls.bp.PORT_D = "PORT_D"
        cls.bp.PORT_1 = "PORT_1"
        cls.bp.PORT_2 = "PORT_2"
        cls.bp.PORT_3 = "PORT_3"
        cls.bp.PORT_4 = "PORT_4"
        cls.bp.SENSOR_TYPE = MagicMock()
        cls.bp.SENSOR_TYPE.EV3_INFRARED_PROXIMITY = "EV3_INFRARED_PROXIMITY"
        cls.bp.SENSOR_TYPE.TOUCH = "TOUCH"
        cls.bp.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS = "EV3_COLOR_COLOR_COMPONENTS"

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_turn_left_after_bump(self, patched_time_sleep):
        pars = {"standard_speed": -50, "super_speed": False}
        DifferentMapLayout.turn_left_after_bump(self.bp, pars)
        # L:50 R:-50
        expected_calls = [
            unittest.mock.call('PORT_D', 50),  # Left motor
            unittest.mock.call('PORT_A', -50),  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(
            expected_calls, any_order=False)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_turn_right_after_bump(self, patched_time_sleep):
        pars = {"standard_speed": -75, "super_speed": False}
        DifferentMapLayout.turn_right_after_bump(self.bp, pars)
        # L:50 R:-50
        expected_calls = [
            unittest.mock.call('PORT_D', -75),  # Left motor
            unittest.mock.call('PORT_A', 75),  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(
            expected_calls, any_order=False)

    def test_smooth_left_turn_on_bridge(self):
        pars = {"standard_speed": -30, "bridgesmoothness": 2,
                "turn_speed": -16, "smoothness": 5, "turn_factor": 1.6}
        left_speed, right_speed = -30, -30
        left_speed_result, right_speed_result = DifferentMapLayout.smooth_left_turn_on_bridge(
            left_speed, right_speed, pars)
        self.assertEqual(left_speed_result, -28.4)
        self.assertEqual(right_speed_result, -31.6)

    def test_smooth_right_turn_on_bridge(self):
        pars = {"standard_speed": -30, "bridgesmoothness": 2,
                "turn_speed": -16, "smoothness": 5, "turn_factor": 1.6}
        left_speed, right_speed = -30, -30
        left_speed_result, right_speed_result = DifferentMapLayout.smooth_right_turn_on_bridge(
            left_speed, right_speed, pars)
        self.assertEqual(left_speed_result, -31.6)
        self.assertEqual(right_speed_result, -28.4)


if __name__ == "__main__":
    unittest.main()
