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

def show_found_black():
    """No light - robot is searching."""
    show_solid([0, 0, 0])

def show_obstacle():
    """Flash white - obstacle detected."""
    show_flash([255, 255, 255], flashes=3)

def show_found_white(color):
    """White scanning pattern - following border, flashes the color its looking for."""
    for i in range(8):
        ws.write_all([0, 0, 0])
        if color == Red:
            ws[i] = [200, 0, 0]
        elif color == Green:
            ws[i] = [0, 200, 0]
        else:
            ws[i] = [0, 0, 200]
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(200)
        
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

def show_found_green():
    """A green-themed celebration pattern."""
    for i in range(5):
        ws.write_all([0, 0, 0])
        show_flash([0,255,0],3,100,100)
        ws[i] = [255, 0, 0]
        time.sleep_ms(1000)
        show_flash([0,255,0],3,100,100)
        time.sleep_ms(10)
        ws.write()
        time.sleep_ms(100)
    pass
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
# Test each pattern
print("Testing white...")
show_found_white()
time.sleep(2)

print("Testing obstacle...")
show_obstacle()
time.sleep(1)

print("Testing black...")
for _ in range(3):
    show_found_black()

print("Testing red...")
show_found_red()
time.sleep(1)

print("Testing green...")
show_found_green()
time.sleep(1)

print("Testing blue...")
show_found_blue()
time.sleep(1)

# Turn off
ws.write_all([0, 0, 0])
ws.write()
print("Done!")
