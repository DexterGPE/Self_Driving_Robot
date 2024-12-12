import unittest
from unittest.mock import patch, Mock
from src.main.Manual_Driving import manual_driving


class TestManualDriving(unittest.TestCase):

    def setUp(self):
        self.bp = Mock()  # Mock BrickPi instance
        self.key_states = {}

    def test_move_forward(self):
        self.key_states["up"] = True
        manual_driving(self.bp, self.key_states)
        self.bp.set_motor_power.assert_called_with(self.bp, -60, -60)

    def test_move_backward(self):
        self.key_states["down"] = True
        manual_driving(self.bp, self.key_states)
        self.bp.set_motor_power.assert_called_with(self.bp, 60, 60)

    def test_turn_right(self):
        self.key_states["right"] = True
        manual_driving(self.bp, self.key_states)
        self.bp.set_motor_power.assert_called_with(self.bp, -20, 20)

    def test_turn_left(self):
        self.key_states["left"] = True
        manual_driving(self.bp, self.key_states)
        self.bp.set_motor_power.assert_called_with(self.bp, 20, -20)

    def test_blade_on(self):
        self.key_states["space"] = True
        manual_driving(self.bp, self.key_states)
        self.bp.set_blade_power.assert_called_with(self.bp, 100)

    def test_stop(self):
        self.key_states["lshift"] = True
        manual_driving(self.bp, self.key_states)
        self.bp.set_motor_power.assert_called_with(self.bp, 0, 0)
        self.bp.set_blade_power.assert_called_with(self.bp, 0)


if __name__ == '__main__':
    unittest.main()
