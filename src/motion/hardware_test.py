from PicoRobotics import KitronikPicoRobotics
from lcd1602 import LCD
import time

board = KitronikPicoRobotics()
lcd = LCD()
time.sleep(0.1)

try:
    lcd.clear()
    lcd.write(0, 0, "Hardware Test")
    lcd.write(0, 1, "Starting...")
    time.sleep(2)
    
    # Test right motor
    lcd.clear()
    lcd.write(0, 0, "Testing Motor 1")
    board.motorOn(1, "f", 50)
    time.sleep(2)
    board.motorOff(1)
    
    # Test left motor
    lcd.write(0, 0, "Testing Motor 2")
    board.motorOn(2, "f", 50)
    time.sleep(2)
    board.motorOff(2)
    
    lcd.clear()
    lcd.write(0, 0, "Test Complete!")

except:
    board.motorOff(1)
    board.motorOff(2)
    lcd.clear()
    lcd.write(0, 0, "Test Failed!")
    raise