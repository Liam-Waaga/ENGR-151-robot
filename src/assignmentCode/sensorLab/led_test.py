import machine
from ws2812 import WS2812
import time

ws = WS2812(machine.Pin(28), 8)

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

def show_ready():
    """Solid green - robot is ready."""
    show_solid([0, 255, 0])

def show_obstacle():
    """Flash red - obstacle detected."""
    show_flash([255, 0, 0], flashes=3)

def show_searching():
    """Blue scanning pattern - looking for target."""
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [0, 0, 255]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(80)

def show_found_red():
    """TODO: Create a red-themed celebration pattern.
    Should last 2-3 seconds and clearly use red colors.
    """
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 0, 0]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(80)
    pass

# Test each pattern
print("Testing ready...")
show_ready()
time.sleep(2)

print("Testing obstacle...")
show_obstacle()
time.sleep(1)

print("Testing searching...")
for _ in range(3):
    show_searching()

print("Testing found_red...")
show_found_red()
time.sleep(1)

# Turn off
ws.write_all([0, 0, 0])
ws.write()
print("Done!")