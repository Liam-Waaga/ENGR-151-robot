import machine
import time
from ws2812 import WS2812

#LED Strip
ws = WS2812(machine.Pin(28), 8)

#Displays a solid color of choice.
def show_solid(color):
    """Display solid color on all LEDs."""
    ws.write_all(color)
    ws.write()

#Displays a flashing color of choice.
def show_flash(color, flashes=3, on_ms=200, off_ms=200):
    """Flash all LEDs a specified number of times."""
    for _ in range(flashes):
        ws.write_all(color)
        ws.write()
        time.sleep_ms(on_ms)
        ws.write_all([0, 0, 0])
        ws.write()
        time.sleep_ms(off_ms)

#What to do when black is found.
def show_found_black():
    """No light - robot is searching."""
    show_solid([0, 0, 0])

#What to do when a bumper is activated.
def show_obstacle():
    """Flash white - obstacle detected."""
    show_flash([255, 255, 255], flashes=2)

#What to do when white is found.
def show_found_white():
    """White scanning pattern - following border, flashes the color its looking for."""
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [200, 200, 200]
        time.sleep_ms(20)
        ws.write()
        time.sleep_ms(20)
    ws.write_all([0, 0, 0])
