from PicoRobotics import KitronikPicoRobotics
import PicoRobotics
from lcd1602 import LCD
from machine import I2C
import time
 


print("1")
board = PicoRobotics.KitronikPicoRobotics()
print("2")
lcd = LCD()
print("3")
time.sleep(0.1)
print("4")

try:
    print("5")
    lcd.clear()
    lcd.write(0, 0, "Hardware Test")
    lcd.write(0, 1, "Starting...")
    time.sleep(2)
    
    print("6")
    
    # Test right motor
    lcd.clear()
    lcd.write(0, 0, "Testing Motor 1")
    board.motorOn(1, "f", 21)
    time.sleep(2)
    board.motorOff(1)
    
    print("7")
    
    # Test left motor
    lcd.write(0, 0, "Testing Motor 2")
    board.motorOn(2, "f", 50)
    time.sleep(2)
    board.motorOff(2)
    
    print("8")
    
    lcd.clear()
    lcd.write(0, 0, "Test Complete!")

except:
    
    print("except")
    
    board.motorOff(1)
    board.motorOff(2)
    lcd.clear()
    lcd.write(0, 0, "Test Failed!")
    raise