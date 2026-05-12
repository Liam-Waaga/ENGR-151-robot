from PicoRobotics import KitronikPicoRobotics
from machine import Pin
from lcd1602 import LCD
import time

board = KitronikPicoRobotics()
lcd = LCD()
time.sleep(0.1)

# Encoder setup
LEFT_ENCODER = Pin(22, Pin.IN, Pin.PULL_UP)
RIGHT_ENCODER = Pin(10, Pin.IN, Pin.PULL_UP)

left_ticks = 0
right_ticks = 0

def left_tick_handler(pin):
    global left_ticks
    left_ticks += 1

def right_tick_handler(pin):
    global right_ticks
    right_ticks += 1

LEFT_ENCODER.irq(trigger=Pin.IRQ_FALLING, handler=left_tick_handler)
RIGHT_ENCODER.irq(trigger=Pin.IRQ_FALLING, handler=right_tick_handler)

def reset_ticks():
    global left_ticks, right_ticks
    left_ticks = 0
    right_ticks = 0

# Distance constants
WHEEL_DIAMETER = 67  # mm
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * 3.14159
WHEEL_DISTANCE = 130
MM_PER_TICK = WHEEL_CIRCUMFERENCE / 20
TICKS_PER_MM = 20 / WHEEL_CIRCUMFERENCE

def drive_distance_mm(target_mm, speed=50, reverse=False): # 50 is good speed
    """Drive forward a specified distance in millimeters."""
    target_ticks = int(target_mm * TICKS_PER_MM)
    reset_ticks()
    
    lcd.clear()
    lcd.write(0, 0, f"Target: {target_mm}mm")
    
    board.motorOn(1, ("r" if reverse else "f"), speed)
    board.motorOn(2, ("r" if reverse else "f"), speed)
    
    while (left_ticks + right_ticks) / 2 < target_ticks:
        avg_ticks = (left_ticks + right_ticks) / 2
        current_mm = avg_ticks * MM_PER_TICK
        lcd.write(0, 1, f"Now: {current_mm:.0f}mm   ")
        time.sleep(0.05)
    
    board.motorOff(1)
    board.motorOff(2)
    
    lcd.clear()
    lcd.write(0, 0, "Done!")
    final_mm = ((left_ticks + right_ticks) / 2) * MM_PER_TICK
    lcd.write(0, 1, f"Traveled: {final_mm:.0f}mm")

'''
def drive_turn(target_mm, direction, base_speed=35):
    target_ticks = int(target_mm * TICKS_PER_MM)
    reset_ticks()
    
    left_speed = base_speed
    right_speed = base_speed
    while (left_ticks + right_ticks) / 2 <= target_ticks:
        print(str((left_ticks + right_ticks) / 2) + " / " + str(target_ticks))
        if direction == "left":
            board.motorOn(1, "f", right_speed)
            board.motorOn(2, "r", left_speed)
        elif direction == "right":
            board.motorOn(1, "r", right_speed)
            board.motorOn(2, "f", left_speed)
    
    board.motorOff(2)
    board.motorOff(1)
    time.sleep(1)
'''

def drive_turn(angle):
    target_ticks = int(target_mm * TICKS_PER_MM)
    reset_ticks()
    
    left_speed = base_speed
    right_speed = base_speed
    while (left_ticks + right_ticks) / 2 <= target_ticks:
        print(str((left_ticks + right_ticks) / 2) + " / " + str(target_ticks))
        if direction == "left":
            board.motorOn(1, "f", right_speed)
            board.motorOn(2, "r", left_speed)
        elif direction == "right":
            board.motorOn(1, "r", right_speed)
            board.motorOn(2, "f", left_speed)
    
    board.motorOff(2)
    board.motorOff(1)
    time.sleep(1) 


def __motor_test():
    # Test: Drive 300mm (about 1 foot)
    try:
        drive_distance_mm(800)
        drive_distance_mm(800, reverse=True)
    except:
        board.motorOff(1)
        board.motorOff(2)
        raise

