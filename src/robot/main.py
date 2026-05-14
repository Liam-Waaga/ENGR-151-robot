import motion
import sensors
import leds
import dancy

def main():
    hit_red = False
    hit_green = False
    hit_blue = False

    while True():
        color = sensors.get_color() # should only return from the following: white, black, red, green, blue

        if color == "black":
            motion.turn_deg(-15)
        elif color == "white":
            motion.turn_deg(15)
        elif color == "red":
            if not hit_red:
                dancy.dance_red()
                hit_red = True
            else:
                motion.turn_deg(90)
        elif color == "green":
            if not hit_green:
                dancy.dance_green()
                hit_green = True
            else:
                motion.turn_deg(90)
        elif color == "blue":
            if not hit_blue:
                dancy.dance_blue()
                hit_blue = True
            else:
                motion.turn_deg(90)
        else:
            dancy.panic()

        # Victory
        if hit_red and hit_green and hit_blue:
            motion.turn_deg(45)
            motion.drive_mm(400)
            dancy.victory()
        else:
            motion.drive_mm(200)

if __name__ == "__main__":
    main()