import motion
import sensors
import leds


def init():
    """
    do initialization code
    """
    pass



def main():
    init()
    
    while True():
        sensors.do_sensor_readings() # this is all of the sensor readings

        if sensors.should_do_dance(): # this pretty much just checks if the color below is a destination
            motion.do_dance(sensors.get_color())
        elif sensors.finished():
            motion.do_victory()
            break
        else:
            motion.do_motion_step()
        

if __name__ == "__main__":
    main()