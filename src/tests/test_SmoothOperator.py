import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append('../main')
sys.path.append('./main')
sys.path.append('..')
sys.path.append('./src/main')

# Mock the brickpi3 module
with (patch.dict('sys.modules', {'brickpi3': MagicMock()})):
    import brickpi3
    from main.SmoothOperator import SmoothOperator


class TestSmoothOperator(unittest.TestCase):

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

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_smooth_left_turn_on_bridge(self, patched_time_sleep):
        speed_left, speed_right = -30, -30
        pars = {"standard_speed": -30, "turn_speed": -15,
                "smoothness": 5, "bridgesmoothness": 2}

        speed_left, speed_right = SmoothOperator.smooth_left_turn_on_bridge(
            speed_left, speed_right, pars)

        self.assertEqual(-28.5, speed_left)
        self.assertEqual(-31.5, speed_right)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_smooth_right_turn_on_bridge(self, patched_time_sleep):
        speed_left, speed_right = -30, -30
        pars = {"standard_speed": -30, "turn_speed": -15,
                "smoothness": 5, "bridgesmoothness": 2}

        speed_left, speed_right = SmoothOperator.smooth_right_turn_on_bridge(
            speed_left, speed_right, pars)

        self.assertEqual(-31.5, speed_left)
        self.assertEqual(-28.5, speed_right)

    def test_red_line_not_found_same_for_rgb(self):
        self.bp.get_sensor.return_value = (30, 30, 30)

        result = SmoothOperator.red_line_found(self.bp)

        self.assertFalse(result)

    def test_red_line_not_found_different_rgb_but_not_red(self):
        self.bp.get_sensor.return_value = (45, 30, 60)

        result = SmoothOperator.red_line_found(self.bp)

        self.assertFalse(result)

    def test_red_line_found(self):
        self.bp.get_sensor.return_value = (100, 0, 0)

        result = SmoothOperator.red_line_found(self.bp)

        self.assertTrue(result)

    def test_detect_that_no_black_found(self):
        self.bp.get_sensor.return_value = (100, 0, 0)

        result = SmoothOperator.detect_black(self.bp)

        self.assertFalse(result)

    def test_detect_that_black_is_found(self):
        self.bp.get_sensor.return_value = (0, 0, 0)

        result = SmoothOperator.detect_black(self.bp)

        self.assertTrue(result)

    def test_detect_that_black_is_found_with_close_values(self):
        self.bp.get_sensor.return_value = (30, 40, 20)

        result = SmoothOperator.detect_black(self.bp)

        self.assertTrue(result)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_reverse_after_bump_without_sleep(self, patched_time_sleep):
        pars = {"standard_speed": -60, "super_speed": True}

        SmoothOperator.reverse_after_bump(self.bp, pars)

        expected_calls = [
            unittest.mock.call('PORT_D', 60),  # Left motor
            unittest.mock.call('PORT_A', 60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=False)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_reverse_after_bump_with_sleep(self, patched_time_sleep):
        pars = {"standard_speed": -60, "super_speed": False}

        SmoothOperator.reverse_after_bump(self.bp, pars)

        expected_calls = [
            unittest.mock.call('PORT_D', 60),  # Left motor
            unittest.mock.call('PORT_A', 60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=False)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_smooth_turn_at_wall_to_move_away(self, patched_time_sleep):
        pars = {"standard_speed": -60, "turn_speed": -30,
                "smoothness": 5, "distance_to_wall": 10}
        self.bp.get_sensor.return_value = 5

        speed_left_result, speed_right_result = (
            SmoothOperator.smooth_turn_at_wall(self.bp, pars))

        self.assertEqual(-30, speed_left_result)
        self.assertEqual(-90, speed_right_result)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_perfect_distance_to_wall_no_turn(self, patched_time_sleep):
        pars = {"standard_speed": -60, "turn_speed": -30,
                "smoothness": 5, "distance_to_wall": 10}
        self.bp.get_sensor.return_value = 10

        speed_left_result, speed_right_result = (
            SmoothOperator.smooth_turn_at_wall(self.bp, pars))

        self.assertEqual(-60, speed_left_result)
        self.assertEqual(-60, speed_right_result)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_smooth_turn_at_wall_to_move_closer(self, patched_time_sleep):
        pars = {"standard_speed": -60, "turn_speed": -30,
                "smoothness": 5, "distance_to_wall": 10}
        self.bp.get_sensor.return_value = 20

        speed_left_result, speed_right_result = (
            SmoothOperator.smooth_turn_at_wall(self.bp, pars))

        self.assertEqual(-90, speed_left_result)
        self.assertEqual(-30, speed_right_result)

    def test_turn_left(self):
        pars = {"standard_speed": -60}

        speed_left_result, speed_right_result = SmoothOperator.turn_left(pars)

        self.assertEqual(60, speed_left_result)
        self.assertEqual(-60, speed_right_result)

    def test_turn_right(self):
        pars = {"standard_speed": -60}

        speed_left_result, speed_right_result = SmoothOperator.turn_right(pars)

        self.assertEqual(-60, speed_left_result)
        self.assertEqual(60, speed_right_result)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_turn_left_after_bump(self, patched_time_sleep):
        pars = {"standard_speed": -60, "super_speed": True}

        SmoothOperator.turn_left_after_bump(self.bp, pars)

        expected_calls = [
            unittest.mock.call('PORT_D', 60),  # Left motor
            unittest.mock.call('PORT_A', -60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=False)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_turn_right_after_bump(self, patched_time_sleep):
        pars = {"standard_speed": -60, "super_speed": True}

        SmoothOperator.turn_right_after_bump(self.bp, pars)

        expected_calls = [
            unittest.mock.call('PORT_D', -60),  # Left motor
            unittest.mock.call('PORT_A', 60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=False)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_choose_to_reverse_and_turn_right_after_bump(self, patched_time_sleep):
        pars = {"standard_speed": -60, "super_speed": True, "distance_to_wall": 30}
        self.bp.get_sensor.return_value = 20

        SmoothOperator.turn_after_bump(self.bp, pars)

        expected_calls = [
            unittest.mock.call('PORT_D', 60),  # Left motor
            unittest.mock.call('PORT_A', 60),  # Right motor
            unittest.mock.call('PORT_D', 60),  # Left motor
            unittest.mock.call('PORT_A', -60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=False)

    @patch('time.sleep', return_value=0)  # Disable sleep() calls
    def test_choose_to_reverse_and_turn_left_after_bump(self, patched_time_sleep):
        pars = {"standard_speed": -60, "super_speed": True, "distance_to_wall": 30}
        self.bp.get_sensor.return_value = 40

        SmoothOperator.turn_after_bump(self.bp, pars)

        expected_calls = [
            unittest.mock.call('PORT_D', 60),  # Left motor
            unittest.mock.call('PORT_A', 60),  # Right motor
            unittest.mock.call('PORT_D', -60),  # Left motor
            unittest.mock.call('PORT_A', 60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=False)


if __name__ == '__main__':
    unittest.main()
