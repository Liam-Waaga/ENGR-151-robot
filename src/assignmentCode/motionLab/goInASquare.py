from PicoRobotics import KitronikPicoRobotics
from machine import Pin
from lcd1602 import LCD
import time

board = KitronikPicoRobotics()
lcd = LCD()
time.sleep(0.1)

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

WHEEL_CIRCUMFERENCE = 67 * 3.14159
MM_PER_TICK = WHEEL_CIRCUMFERENCE / 20
TICKS_PER_MM = 20 / WHEEL_CIRCUMFERENCE

def drive_straight_mm(target_mm, base_speed=50):
    """Drive forward with correction to maintain straight line."""
    target_ticks = int(target_mm * TICKS_PER_MM)
    reset_ticks()
    
    left_speed = base_speed
    right_speed = base_speed
    correction = 5  # Speed adjustment amount
    
    board.motorOn(1, "f", right_speed)
    board.motorOn(2, "f", left_speed)
    
    while (left_ticks + right_ticks) / 2 < target_ticks:
        # Compare wheel progress
        diff = left_ticks - right_ticks
        
        # Adjust speeds to correct drift
        if diff > 2:  # Left wheel ahead, slow it down
            left_speed = base_speed - correction
            right_speed = base_speed + correction
        elif diff < -2:  # Right wheel ahead, slow it down
            left_speed = base_speed + correction
            right_speed = base_speed - correction
        else:
            left_speed = base_speed
            right_speed = base_speed
        
        # Keep speeds in valid range
        left_speed = max(20, min(100, left_speed))
        right_speed = max(20, min(100, right_speed))
        
        board.motorOn(1, "f", right_speed)
        board.motorOn(2, "f", left_speed)
        
        lcd.clear()
        lcd.write(0, 0, f"L:{left_ticks} R:{right_ticks}")
        lcd.write(0, 1, f"Diff: {diff}")
        time.sleep(0.07)
    
    board.motorOff(1)
    board.motorOff(2)
    time.sleep(1)

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

try:
    time.sleep(2)
    drive_straight_mm(110)
    drive_turn(105, "right")
    drive_straight_mm(110)
    drive_turn(105, "right")
    drive_straight_mm(110)
    drive_turn(110, "right")
    drive_straight_mm(110)
    drive_turn(300, "left")
    lcd.clear()
    lcd.write(0, 0, "Done!")
except:
    board.motorOff(1)
    board.motorOff(2)
    raise