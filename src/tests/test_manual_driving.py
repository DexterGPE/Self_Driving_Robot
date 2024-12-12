import unittest
from unittest.mock import MagicMock, patch

from src.main.Manual_Driving import manual_driving


class TestManualDriving(unittest.TestCase):
    pass
    # @patch('Control_BrickPi.set_motor_power')  # Mock the set_motor_power function
    # @patch('Control_BrickPi.set_blade_power')  # Mock the set_blade_power function
    # def test_manual_driving(self, mock_set_blade_power, mock_set_motor_power):
    #     # Create a mock BrickPi instance
    #     bp = MagicMock()
    #
    #     # Define test cases as (key_states, expected_motor, expected_blade)
    #     test_cases = [
    #         ({"up": True, "down": False, "left": False, "right": False, "space": False, "lshift": False}, (-60, -60), 0),
    #         ({"up": False, "down": True, "left": False, "right": False, "space": False, "lshift": False}, (60, 60), 0),
    #         ({"up": False, "down": False, "left": True, "right": False, "space": False, "lshift": False}, (20, -20), 0),
    #         ({"up": False, "down": False, "left": False, "right": True, "space": False, "lshift": False}, (-20, 20), 0),
    #         ({"up": False, "down": False, "left": False, "right": False, "space": True, "lshift": False}, (0, 0), 100),
    #         ({"up": True, "down": False, "left": False, "right": False, "space": False, "lshift": True}, (0, 0), 0),
    #     ]
    #
    #     for key_states, expected_motor, expected_blade in test_cases:
    #         # Call the function under test
    #         manual_driving(bp, key_states)
    #
    #         # Verify the mocked functions were called with expected arguments
    #         mock_set_motor_power.assert_called_with(bp, *expected_motor)
    #         mock_set_blade_power.assert_called_with(bp, expected_blade)
    #
    #         # Reset mocks for the next iteration
    #         mock_set_motor_power.reset_mock()
    #         mock_set_blade_power.reset_mock()

if __name__ == '__main__':
    unittest.main()


