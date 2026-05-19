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

#What to do when red is found.
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

#What to do when green is found.
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

#What to do when blue is found.
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

#Finale when all colors have been found. A combination of all colors.
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
