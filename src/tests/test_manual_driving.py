import unittest
from unittest.mock import MagicMock, patch

# Mock the Control_BrickPi module
with patch.dict('sys.modules', {'brickpi3': MagicMock()}):
    import brickpi3
    from main.Control_BrickPi import set_motor_power, set_blade_power
    from main.Manual_Driving import manual_driving


class TestManualDriving(unittest.TestCase):

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

    def test_manual_driving_forwards(self):
        # Simulate pressing the "up" key
        key_states = {"up": True, "down": False, "right": False, "left": False, "space": False, "lshift": False}
        manual_driving(self.bp, key_states)

        # Verify that set_motor_power was called for PORT_D and PORT_A
        expected_calls = [
            unittest.mock.call('PORT_D', -60),  # Left motor
            unittest.mock.call('PORT_A', -60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=True)


    def test_manual_driving_backwards(self):
        # Simulate pressing the "up" key
        key_states = {"up": False, "down": True, "right": False, "left": False, "space": False, "lshift": False}
        manual_driving(self.bp, key_states)

        # Verify that set_motor_power was called for PORT_D and PORT_A
        expected_calls = [
            unittest.mock.call('PORT_D', +60),  # Left motor
            unittest.mock.call('PORT_A', +60)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=True)

    def test_manual_driving_left(self):
        # Simulate pressing the "left" key
        key_states = {"up": False, "down": False, "right": False, "left": True, "space": False, "lshift": False}
        manual_driving(self.bp, key_states)

        # Verify that set_motor_power was called for PORT_D and PORT_A
        expected_calls = [
            unittest.mock.call('PORT_D', +40),  # Left motor
            unittest.mock.call('PORT_A', -40)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=True)

    def test_manual_driving_right(self):
        # Simulate pressing the "right" key
        key_states = {"up": False, "down": False, "right": True, "left": False, "space": False, "lshift": False}
        manual_driving(self.bp, key_states)

        # Verify that set_motor_power was called for PORT_D and PORT_A
        expected_calls = [
            unittest.mock.call('PORT_D', -40),  # Left motor
            unittest.mock.call('PORT_A', +40)  # Right motor
        ]
        self.bp.set_motor_power.assert_has_calls(expected_calls, any_order=True)

    # def test_manual_driving_blade(self):
    #     # Simulate pressing the "space" key
    #     key_states = {"up": False, "down": False, "right": False, "left": False, "space": True, "lshift": False}
    #     manual_driving(self.bp, key_states)
    #
    #     # Verify that set_motor_power was called for PORT_D and PORT_A
    #     expected_call = [unittest.mock.call('PORT_B', +50)]
    #     self.bp.set_blade_power.assert_has_calls(expected_call, any_order=True)
    #
    # def test_manual_driving_lshift(self):
    #     # Simulate pressing the "lshift" key
    #     key_states = {"up": False, "down": False, "right": False, "left": False, "space": False, "lshift": True}
    #     manual_driving(self.bp, key_states)
    #
    #     # Assert all motors and blade were stopped
    #     set_motor_power.assert_called_once_with(self.bp, 0, 0)
    #     set_blade_power.assert_called_once_with(self.bp, 0)
    #
    # def test_no_key_pressed(self):
    #     # Simulate no key pressed
    #     key_states = {"up": False, "down": False, "right": False, "left": False, "space": False, "lshift": False}
    #     manual_driving(self.bp, key_states)
    #
    #     # Assert no motor or blade power was set
    #     set_motor_power.assert_called_once_with(self.bp, 0, 0)
    #     set_blade_power.assert_called_once_with(self.bp, 0)


if __name__ == "__main__":
    unittest.main()
