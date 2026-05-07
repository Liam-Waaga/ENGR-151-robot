from machine import Pin
from lcd1602 import LCD
import time

lcd = LCD()
time.sleep(0.1)

# Configure bump sensors with internal pull-ups
front_bump = Pin(17, Pin.IN, Pin.PULL_UP)
rear_bump = Pin(16, Pin.IN, Pin.PULL_UP)

lcd.clear()
lcd.write(0, 0, "Bump Sensor Test")
time.sleep(2)

while True:
    front_pressed = front_bump.value() == 0  # LOW when pressed
    rear_pressed = rear_bump.value() == 0
    
    lcd.clear()
    
    if front_pressed:
        lcd.write(0, 0, "FRONT: PRESSED")
    else:
        lcd.write(0, 0, "FRONT: --")
    
    if rear_pressed:
        lcd.write(0, 1, "REAR:  PRESSED")
    else:
        lcd.write(0, 1, "REAR:  --")
    
    time.sleep(0.1)