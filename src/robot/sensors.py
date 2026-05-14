import machine
from machine import Pin, I2C
import leds
import time
from color_sensor import ColorSensor
from lcd1602 import LCD
from ws2812 import WS2812

#LCD
lcd = LCD()
time.sleep(0.1)

#Bump Sensors
front_bump = Pin(17, Pin.IN, Pin.PULL_UP)
rear_bump = Pin(16, Pin.IN, Pin.PULL_UP)

# Initialize I2C and sensor
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
sensor = ColorSensor(i2c)

sensor.BLACK_THRESHOLD = 1052      # Your measured value
sensor.WHITE_MIN_CLEAR = 9835    # From calibrate_white output
sensor.WHITE_MAX_RATIO_SPREAD = 70.6  # From calibrate_white output

#Variables
frontBumperCount = 0
backBumperCount = 0
Redcheck = True
Greencheck = True
Bluecheck = True


def show_solid(color):
    """Display solid color on all LEDs."""
    ws.write_all(color)
    ws.write()

def show_flash(color, flashes=3, on_ms=200, off_ms=200):
    """Flash all LEDs a specified number of times."""
    for _ in range(flashes):
        ws.write_all(color)
        ws.write()
        time.sleep_ms(on_ms)
        ws.write_all([0, 0, 0])
        ws.write()
        time.sleep_ms(off_ms)

def motor_sensor():
    currentColor = sensor.get_color()[0]
    return currentColor

while True:
    #Bump counter
    front_pressed = front_bump.value() == 0
    rear_pressed = rear_bump.value() == 0
    ws.write_all([0, 0, 0])
    
    if front_pressed:
        frontBumperCount += 1
    lcd.write(0, 0, "FRONT: " + str(frontBumperCount))
    
    if rear_pressed:
        backBumperCount += 1

    lcd.write(0, 1, "REAR: " + str(backBumperCount))
    
    #if color do this
    currentColor = sensor.get_color()[0]
    print(str(currentColor))
    if currentColor == "Red" and Redcheck == True:
        Redcheck = False
        show_found_red()
    elif currentColor == "Green" and Greencheck == True:
        Greencheck = False
        show_found_green()
    elif currentColor == "Blue" and Bluecheck == True:
        Bluecheck = False
        show_found_blue()
    elif currentColor == "White":
        show_found_white()
    elif currentColor == "Black":
        show_found_black()
    
    #if bump flash
    if front_pressed or rear_pressed:
        show_obstacle()
    
    time.sleep(0.1)
    
