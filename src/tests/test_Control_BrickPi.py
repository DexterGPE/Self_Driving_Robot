import unittest
import brickpi3


class TestBrickPi3Functions(unittest.TestCase):

    def setUp(self):
        # Initialize the BrickPi3 instance for testing
        self.bp = brickpi3.BrickPi3()

    def test_set_motor_power(self):
        # Test setting motor power
        set_motor_power(self.bp, 100, 200)
        self.assertEqual(self.bp.get_motor_power(self.bp.PORT_D), 100)
        self.assertEqual(self.bp.get_motor_power(self.bp.PORT_A), 200)

    def test_set_blade_power(self):
        # Test setting blade power
        set_blade_power(self.bp, 150)
        self.assertEqual(self.bp.get_motor_power(self.bp.PORT_B), 150)

    def test_initialize_brickpi_sensors(self):
        # Test sensor initialization
        bp = initialize_brickpi_sensors()
        self.assertEqual(bp.get_sensor_type(bp.PORT_1), bp.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
        self.assertEqual(bp.get_sensor_type(bp.PORT_2), bp.SENSOR_TYPE.TOUCH)
        self.assertEqual(bp.get_sensor_type(bp.PORT_3), bp.SENSOR_TYPE.TOUCH)
        self.assertEqual(bp.get_sensor_type(bp.PORT_4), bp.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)


if __name__ == '__main__':
    unittest.main()
