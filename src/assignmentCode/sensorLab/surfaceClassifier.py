import machine
from machine import Pin, I2C
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

#LED Strip
ws = WS2812(machine.Pin(28), 8)

# Initialize I2C and sensor
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
sensor = ColorSensor(i2c)

sensor.BLACK_THRESHOLD = 1052      # Your measured value
sensor.WHITE_MIN_CLEAR = 9835    # From calibrate_white output
sensor.WHITE_MAX_RATIO_SPREAD = 70.6  # From calibrate_white output

#Variables
frontBumperCount = 0
backBumperCount = 0

#found red
def show_found_red():
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 0, 0]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(80)
    pass

#found blue
def show_found_green():
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [0, 255, 0]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(20)
    pass

#found green
def show_found_blue():
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [0, 0, 255]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(20)
    pass

#tape border
def show_found_white():
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 255, 255]
        time.sleep_ms(10)  # Brief pause for electronics
        ws.write()
        time.sleep_ms(100)
    # Backward
    for i in range(6, 0, -1):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 255, 255]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(100)
    pass
#black floor
def show_found_black():
    ws.write_all([0, 0, 0])
    pass
#warning flash
def bumper_flash():
    ws.write_all([100, 100, 100])
    pass

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
    if currentColor == "Red":
        show_found_red()
    elif currentColor == "Green":
        show_found_green()
    elif currentColor == "Blue":
        show_found_blue()
    elif currentColor == "White":
        show_found_white()
    elif currentColor == "Black":
        show_found_black()
    
    #if bump flash
    if front_pressed or rear_pressed:
        bumper_flash()
    
    time.sleep(0.1)
    