from machine import Pin, I2C
from color_sensor import ColorSensor
import time

# Initialize sensor
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)
sensor = ColorSensor(i2c)

print("=== Color Sensor Calibration ===")
print()

# Step 1: Calibrate white (uses built-in function)
print("STEP 1: White Calibration")
print("Position sensor over WHITE tape at the height it will be mounted on your robot.")
input("Press Enter when ready...")

calibration = sensor.calibrate_white(samples=10)
print()

# Step 2: Measure black floor for BLACK_THRESHOLD
print("STEP 2: Black Floor Measurement")
print("Position sensor over BLACK arena floor at mounting height.")
input("Press Enter when ready...")

print("Taking 10 readings...")
clear_values = []
for i in range(10):
    _, _, _, c = sensor.get_raw_data()
    clear_values.append(c)
    print(f"  Reading {i+1}: Clear = {c}")
    time.sleep(0.2)

avg_black_clear = sum(clear_values) / len(clear_values)
suggested_black_threshold = int(avg_black_clear * 1.5)  # Add margin

print()
print(f"Average black clear value: {avg_black_clear:.0f}")
print(f"Suggested BLACK_THRESHOLD: {suggested_black_threshold}")
print()

# Apply the black threshold
sensor.BLACK_THRESHOLD = suggested_black_threshold
print(f"Applied BLACK_THRESHOLD = {sensor.BLACK_THRESHOLD}")

# Step 3: Verify calibration
print()
print("STEP 3: Verification")
print("Test each surface to verify detection works.")
print("Press Ctrl+C to exit.")
print()

while True:
    color, confidence, (r, g, b, c) = sensor.get_color()
    print(f"Detected: {color:10} | Confidence: {confidence:.2f} | Clear: {c}")
    time.sleep(0.5)
    