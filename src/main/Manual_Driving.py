import Control_BrickPi


def manual_driving(bp, key_states):
    speed_left = 0
    speed_right = 0
    speed_blade = 0

    if key_states["up"]:
        speed_left -= 100
        speed_right -= 100
    if key_states["down"]:
        speed_left += 100
        speed_right += 100
    if key_states["right"]:
        speed_right += 40
        speed_left -= 40
    if key_states["left"]:
        speed_right -= 40
        speed_left += 40
    if key_states["space"]:
        speed_blade = 50
    if key_states["lshift"]:
        speed_left = 0
        speed_right = 0
        speed_blade = 0

    Control_BrickPi.set_motor_power(bp, speed_left, speed_right)
    Control_BrickPi.set_blade_power(bp, speed_blade)
