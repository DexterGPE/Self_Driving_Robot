import brickpi3


def set_motor_power(bp, speed_left, speed_right):
    bp.set_motor_power(bp.PORT_D, speed_left)
    bp.set_motor_power(bp.PORT_A, speed_right)


def set_blade_power(bp, speed_blade):
    bp.set_motor_power(bp.PORT_B, speed_blade)


def initialize_brickpi_sensors():
    bp = brickpi3.BrickPi3()  # Create an instance of the BrickPi3 class.

    bp.set_sensor_type(bp.PORT_1, bp.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
    bp.set_sensor_type(bp.PORT_2, bp.SENSOR_TYPE.TOUCH)
    bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.TOUCH)
    bp.set_sensor_type(bp.PORT_4, bp.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)
    return bp


def get_red(bp):
    return bp.get_sensor(bp.PORT_4)[0]


def get_green(bp):
    return bp.get_sensor(bp.PORT_4)[1]


def get_blue(bp):
    return bp.get_sensor(bp.PORT_4)[2]


def get_distance(bp):
    return bp.get_sensor(bp.PORT_1)


def get_left_bumper(bp):
    return bp.get_sensor(bp.PORT_3)


def get_right_bumper(bp):
    return bp.get_sensor(bp.PORT_2)
