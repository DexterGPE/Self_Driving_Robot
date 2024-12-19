import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append('../main')

# Mock the brickpi3 module
with patch.dict('sys.modules', {'brickpi3': MagicMock()}):
    import brickpi3
    from main.Control_BrickPi import set_motor_power, set_blade_power, \
        initialize_brickpi_sensors


class TestBrickPi3Functions(unittest.TestCase):

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

    def test_set_motor_power(self):
        # Call the function
        set_motor_power(self.bp, 100, 200)

        # Verify the motor power was set correctly
        self.bp.set_motor_power.assert_any_call(self.bp.PORT_D, 100)
        self.bp.set_motor_power.assert_any_call(self.bp.PORT_A, 200)

    def test_set_blade_power(self):
        # Call the function
        set_blade_power(self.bp, 150)

        # Verify the blade power was set correctly
        self.bp.set_motor_power.assert_called_once_with(self.bp.PORT_B, 150)

    def test_initialize_brickpi_sensors(self):
        # Call the function
        bp_instance = initialize_brickpi_sensors()

        # Verify the sensor types were set correctly
        self.assertEqual(bp_instance.set_sensor_type.call_count, 4)  # Ensure all sensors are set
        bp_instance.set_sensor_type.assert_any_call(
            bp_instance.PORT_1,
            bp_instance.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
        bp_instance.set_sensor_type.assert_any_call(bp_instance.PORT_2,
                                                    bp_instance.SENSOR_TYPE.TOUCH)
        bp_instance.set_sensor_type.assert_any_call(bp_instance.PORT_3,
                                                    bp_instance.SENSOR_TYPE.TOUCH)
        bp_instance.set_sensor_type.assert_any_call(
            bp_instance.PORT_4,
            bp_instance.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)



if __name__ == "__main__":
    unittest.main()
