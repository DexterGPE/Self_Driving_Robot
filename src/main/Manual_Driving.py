from RobotRunner import set_motor_power, set_blade_power


def manual_driving(bp, key_states):
    speed_left = 0
    speed_right = 0
    speed_blade = 0

    if key_states["up"]:
        speed_left -= 60
        speed_right -= 60
    if key_states["down"]:
        speed_left += 60
        speed_right += 60
    if key_states["right"]:
        speed_right += 20
        speed_left -= 20
    if key_states["left"]:
        speed_right -= 20
        speed_left += 20
    if key_states["space"]:
        speed_blade = 100
    if key_states["lshift"]:
        speed_left = 0
        speed_right = 0
        speed_blade = 0

    set_motor_power(bp, speed_left, speed_right)
    set_blade_power(bp, speed_blade)
