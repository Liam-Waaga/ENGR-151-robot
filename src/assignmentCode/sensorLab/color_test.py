from machine import Pin, I2C
from color_sensor import ColorSensor
import time

# Initialize I2C and sensor
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
sensor = ColorSensor(i2c)

sensor.BLACK_THRESHOLD = 1052      # Your measured value
sensor.WHITE_MIN_CLEAR = 9835    # From calibrate_white output
sensor.WHITE_MAX_RATIO_SPREAD = 70.6  # From calibrate_white output

print("Color Sensor Test")
print("Hold sensor 1-2cm above colored surfaces")
print("-" * 50)

while True:
    color, confidence, (r, g, b, c) = sensor.get_color()
    r_ratio, g_ratio, b_ratio, _ = sensor.get_normalized_values()
    
    print(f"Detected: {color} (confidence: {confidence:.2f})")
    print(f"Raw: R={r}, G={g}, B={b}, C={c}")
    print(f"Normalized: R={r_ratio:.1f}, G={g_ratio:.1f}, B={b_ratio:.1f}")
    print("-" * 50)
    time.sleep(1)