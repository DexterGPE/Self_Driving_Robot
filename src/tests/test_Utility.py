import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append('../main')

with patch.dict('sys.modules', {'brickpi3': MagicMock()}):
    import brickpi3
    from main.Utility import print_sensors


class TestRobotRunner(unittest.TestCase):

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

    def test_print_sensors_valid_data_with_correct_return(self):
        self.bp.get_sensor.side_effect = {
            self.bp.PORT_1: 100,
            self.bp.PORT_4: (255, 0, 0),
            self.bp.PORT_3: True,
            self.bp.PORT_2: False
        }.get

        countdown = 0
        new_countdown = print_sensors(self.bp, countdown)

        self.assertEqual(new_countdown, 49)

    def test_print_sensors_invalid_data(self):
        self.bp.get_sensor.side_effect = {
            self.bp.PORT_1: None,  # invalid wall distance
            self.bp.PORT_4: None,  # invalid color
            self.bp.PORT_3: None,  # invalid left touch pushed
            self.bp.PORT_2: None  # invalid right touch pushed
        }.get

        countdown = 0
        new_countdown = print_sensors(self.bp, countdown)

        self.assertEqual(new_countdown, 49)

    def test_not_printing_high_countdown(self):
        self.bp.get_sensor.side_effect = {
            self.bp.PORT_1: 100,
            self.bp.PORT_4: (255, 0, 0),
            self.bp.PORT_3: True,
            self.bp.PORT_2: False
        }.get

        countdown = 10
        new_countdown = print_sensors(self.bp, countdown)

        self.assertEqual(new_countdown, 9)


if __name__ == '__main__':
    unittest.main()
