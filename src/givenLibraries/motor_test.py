from PicoRobotics import KitronikPicoRobotics
from lcd1602 import LCD
import time

board = KitronikPicoRobotics()
lcd = LCD()
time.sleep(0.1)

try:
    # Test 1: Both motors forward
    lcd.clear()
    lcd.write(0, 0, "Forward")
    board.motorOn(1, "f", 50)
    board.motorOn(2, "f", 50)
    time.sleep(2)
    board.motorOff(1)
    board.motorOff(2)
    time.sleep(1)
    
    # Test 2: Both motors reverse
    lcd.clear()
    lcd.write(0, 0, "Reverse")
    board.motorOn(1, "r", 50)
    board.motorOn(2, "r", 50)
    time.sleep(2)
    board.motorOff(1)
    board.motorOff(2)
    time.sleep(1)
    
    # Test 3: Spin in place (motors opposite directions)
    lcd.clear()
    lcd.write(0, 0, "Spin Right")
    board.motorOn(1, "r", 50)
    board.motorOn(2, "f", 50)
    time.sleep(2)
    board.motorOff(1)
    board.motorOff(2)
    
    lcd.clear()
    lcd.write(0, 0, "Done!")

except:
    board.motorOff(1)
    board.motorOff(2)
    raise