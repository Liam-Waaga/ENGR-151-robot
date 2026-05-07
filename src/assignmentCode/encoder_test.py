from PicoRobotics import KitronikPicoRobotics
from machine import Pin
from lcd1602 import LCD
import time

board = KitronikPicoRobotics()
lcd = LCD()
time.sleep(0.1)

# Encoder pin setup
LEFT_ENCODER = Pin(22, Pin.IN, Pin.PULL_UP)
RIGHT_ENCODER = Pin(10, Pin.IN, Pin.PULL_UP)

# Tick counters
left_ticks = 0
right_ticks = 0

# Interrupt handlers
def left_tick_handler(pin):
    global left_ticks
    left_ticks += 1

def right_tick_handler(pin):
    global right_ticks
    right_ticks += 1

# Attach interrupts
LEFT_ENCODER.irq(trigger=Pin.IRQ_FALLING, handler=left_tick_handler)
RIGHT_ENCODER.irq(trigger=Pin.IRQ_FALLING, handler=right_tick_handler)

def reset_ticks():
    global left_ticks, right_ticks
    left_ticks = 0
    right_ticks = 0

# Test: Turn wheels by hand
lcd.clear()
lcd.write(0, 0, "Turn wheels")
lcd.write(0, 1, "by hand...")
time.sleep(2)

for _ in range(10):
    lcd.clear()
    lcd.write(0, 0, f"L: {left_ticks}")
    lcd.write(0, 1, f"R: {right_ticks}")
    time.sleep(1)