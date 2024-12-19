

def print_sensors(bp, countdown):
    try:
        if countdown == 0:
            print("Wall distance: {0}".format(bp.get_sensor(bp.PORT_1)))
            print("Color: {0}".format(bp.get_sensor(bp.PORT_4)))
            print("Left touch pushed: {0}".format(bp.get_sensor(bp.PORT_3)))
            print("Right touch pushed: {0}".format(bp.get_sensor(bp.PORT_2)))
            countdown = 50
    except (TypeError, AttributeError, IOError) as e:
        print("Invalid sensor data:", e)
    return countdown - 1