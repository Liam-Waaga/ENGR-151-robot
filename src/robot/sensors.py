import machine
from machine import Pin, I2C
import dancy
import leds
import time
from color_sensor import ColorSensor
from lcd1602 import LCD
from ws2812 import WS2812

#LCD
lcd = LCD()
time.sleep(0.1)

#Bump Sensors.
front_bump = Pin(17, Pin.IN, Pin.PULL_UP)
rear_bump = Pin(16, Pin.IN, Pin.PULL_UP)

# Initialize I2C and sensor.
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
sensor = ColorSensor(i2c)

sensor.BLACK_THRESHOLD = 1052      # Your measured value
sensor.WHITE_MIN_CLEAR = 9835    # From calibrate_white output
sensor.WHITE_MAX_RATIO_SPREAD = 70.6  # From calibrate_white output

#Variables for bumpers.
frontBumperCount = 0
backBumperCount = 0

#Check to make sure each of RGB is activated only once.
Redcheck = True
Greencheck = True
Bluecheck = True

#Function for color scanning for motors.
def motor_sensor():
    currentColor = sensor.get_color()[0]
    return currentColor

while True:
    #Bump counter.
    front_pressed = front_bump.value() == 0
    rear_pressed = rear_bump.value() == 0
    ws.write_all([0, 0, 0])
    
    if front_pressed:
        global frontBumperCount
        frontBumperCount += 1
    lcd.write(0, 0, "FRONT: " + str(frontBumperCount))
    
    if rear_pressed:
        global backBumperCount
        backBumperCount += 1

    lcd.write(0, 1, "REAR: " + str(backBumperCount))
    
    #What to do when a color is scanned, calls from the file leds.
    currentColor = sensor.get_color()[0]
    print(str(currentColor))
    if currentColor == "Red" and Redcheck == True:
        Redcheck = False
        dancy.dance_red()
    elif currentColor == "Green" and Greencheck == True:
        Greencheck = False
        dancy.dance_green()
    elif currentColor == "Blue" and Bluecheck == True:
        Bluecheck = False
        dancy.dance_blue()
    elif currentColor == "White":
        leds.show_found_white()
    elif currentColor == "Black":
        dancy.show_found_black()
    
    #If bumper activates, calls from the file leds.
    if front_pressed or rear_pressed:
        leds.show_obstacle()
    
    time.sleep(0.1)
    
