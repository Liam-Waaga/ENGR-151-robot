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

def show_found_black():
    """No light - robot is searching."""
    show_solid([0, 0, 0])

def show_obstacle():
    """Flash white - obstacle detected."""
    show_flash([255, 255, 255], flashes=2)

def show_found_white():
    """White scanning pattern - following border, flashes the color its looking for."""
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [200, 200, 200]
        time.sleep_ms(20)
        ws.write()
        time.sleep_ms(20)
    ws.write_all([0, 0, 0])
        
def show_found_red():
    """A red-themed celebration pattern."""
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 0, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(80)
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [200, 0, 0]
        time.sleep_ms(200)
        ws.write()
        time.sleep_ms(200)
    show_flash([255,0,0],3,500,500)
    pass

def show_found_green():
    """A green-themed celebration pattern."""
    for i in range(3):
        ws.write_all([0, 0, 0])
        show_flash([0,255,0],3,100,100)
        ws[i] = [255, 0, 0]
        time.sleep_ms(1000)
        show_flash([0,255,0],2,50,100)
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(100)
    pass
def show_found_blue():
    """A blue-themed celebration pattern."""
    for i in range(2):
        ws.write_all([0, 0, 0])
        show_flash([0,0,255],5,500,500)
        ws[i] = [0, 80, 180]
        show_flash([50,0,100],3,100,100)
        time.sleep_ms(50)
        ws.write()
        ws[i] = [0, 0, 255]
        time.sleep_ms(100)
    pass

def finale_color():
    ws.write_all([0, 0, 0])
    show_flash([0,0,255],1,500,500)
    show_flash([0,255,0],1,500,500)
    show_flash([255,0,0],1,500,500)
    for i in range(8):
        ws[i] = [0, 0, 255]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(10)
    time.sleep_ms(10)
    for i in range(8):
        ws[i] = [0, 255, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(10)
    time.sleep_ms(10)
    for i in range(8):
        ws[i] = [255, 0, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(10)
    time.sleep_ms(400)
    show_flash([0,0,255],1,200,500)
    show_flash([0,255,0],1,500,500)
    show_flash([255,0,0],1,300,500)
    show_flash([255, 255, 255],3,200,400)
    

def motor_sensor():
    currentColor = sensor.get_color()[0]
    return currentColor

while True:
    finale_color()
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
        show_obstacle()
    
    time.sleep(0.1)
    
