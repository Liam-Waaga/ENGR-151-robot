from machine import Pin, I2C
import time

class ColorSensor:
    """Optimized class for interfacing with TCS34725 RGB color sensor"""
    
    # TCS34725 Constants
    _ADDR = 0x29
    _COMMAND_BIT = 0x80
    _ENABLE = 0x00
    _ATIME = 0x01
    _CONTROL = 0x0F
    _RDATAL = 0x16
    _GDATAL = 0x18
    _BDATAL = 0x1A
    _CDATAL = 0x14
    
    # Color detection thresholds (tunable parameters)
    BLACK_THRESHOLD = 800          # Clear value below this = black
    WHITE_MIN_CLEAR = 3000         # Minimum clear value for white
    WHITE_MAX_RATIO_SPREAD = 25    # Max difference between RGB ratios for white
    COLOR_DOMINANCE_FACTOR = 1.3   # How much a color must dominate others
    WEAK_COLOR_THRESHOLD = 2000    # Clear value below this = weak/uncertain color
    
    def __init__(self, i2c):
        """Initialize the color sensor with the provided I2C bus"""
        self.i2c = i2c
        self._init_sensor()
    
    def _init_sensor(self):
        """Initialize the sensor with appropriate settings"""
        # Power on
        self.i2c.writeto_mem(self._ADDR, self._COMMAND_BIT | self._ENABLE, bytes([0x01]))
        time.sleep(0.003)
        # Enable RGB and Wait time
        self.i2c.writeto_mem(self._ADDR, self._COMMAND_BIT | self._ENABLE, bytes([0x03]))
        # Set integration time (154ms) - using 0xEB instead of 0xC0 for better sensitivity
        self.i2c.writeto_mem(self._ADDR, self._COMMAND_BIT | self._ATIME, bytes([0xEB]))
        # Set gain (4x) - good balance of sensitivity and saturation avoidance
        self.i2c.writeto_mem(self._ADDR, self._COMMAND_BIT | self._CONTROL, bytes([0x01]))
        time.sleep(0.05)
    
    def get_raw_data(self):
        """
        Read raw color values from the sensor.
        Returns:
            tuple: (red, green, blue, clear) raw values
        """
        r = self.i2c.readfrom_mem(self._ADDR, self._COMMAND_BIT | self._RDATAL, 2)
        g = self.i2c.readfrom_mem(self._ADDR, self._COMMAND_BIT | self._GDATAL, 2)
        b = self.i2c.readfrom_mem(self._ADDR, self._COMMAND_BIT | self._BDATAL, 2)
        c = self.i2c.readfrom_mem(self._ADDR, self._COMMAND_BIT | self._CDATAL, 2)
        
        # Convert bytes to integers (little-endian)
        r_val = r[0] + (r[1] << 8)
        g_val = g[0] + (g[1] << 8)
        b_val = b[0] + (b[1] << 8)
        c_val = c[0] + (c[1] << 8)
        
        return r_val, g_val, b_val, c_val
    
    def get_color(self):
        """
        Read and identify the current color using improved algorithm.
        Returns:
            tuple: (color_name, confidence, raw_values)
            where confidence is a float 0-1 indicating detection certainty
        """
        r, g, b, c = self.get_raw_data()
        
        # Handle no light condition
        if c < 100:
            return "No light", 1.0, (r, g, b, c)
        
        # Calculate normalized RGB ratios
        r_ratio = (r / c) * 255 if c > 0 else 0
        g_ratio = (g / c) * 255 if c > 0 else 0
        b_ratio = (b / c) * 255 if c > 0 else 0
        
        # Calculate color metrics
        max_ratio = max(r_ratio, g_ratio, b_ratio)
        min_ratio = min(r_ratio, g_ratio, b_ratio)
        ratio_spread = max_ratio - min_ratio
        avg_ratio = (r_ratio + g_ratio + b_ratio) / 3
        
        # Priority 1: Black detection (low overall light)
        if c < self.BLACK_THRESHOLD:
            confidence = min(1.0, (self.BLACK_THRESHOLD - c) / self.BLACK_THRESHOLD)
            return "Black", confidence, (r, g, b, c)
        
        # Priority 2: White detection (high clear, low ratio spread)
        if (c > self.WHITE_MIN_CLEAR and 
            ratio_spread < self.WHITE_MAX_RATIO_SPREAD and 
            min_ratio > 40):  # All RGB components should be reasonably high
            
            # Calculate white confidence based on ratio spread (lower spread = more confident)
            confidence = max(0.6, 1.0 - (ratio_spread / self.WHITE_MAX_RATIO_SPREAD) * 0.4)
            return "White", confidence, (r, g, b, c)
        
        # Priority 3: Specific color detection
        color, confidence = self._detect_specific_color(r_ratio, g_ratio, b_ratio, c, ratio_spread)
        
        return color, confidence, (r, g, b, c)
    
    def _detect_specific_color(self, r_ratio, g_ratio, b_ratio, c, ratio_spread):
        """
        Detect specific colors using improved logic.
        Returns:
            tuple: (color_name, confidence)
        """
        # Low confidence for weak colors
        base_confidence = min(1.0, c / self.WEAK_COLOR_THRESHOLD) * 0.6 + 0.4
        
        # Find dominant color
        max_ratio = max(r_ratio, g_ratio, b_ratio)
        second_max = sorted([r_ratio, g_ratio, b_ratio])[-2]
        
        # Calculate dominance (how much the max exceeds the second highest)
        if second_max > 0:
            dominance = max_ratio / second_max
        else:
            dominance = float('inf')
        
        # Require sufficient dominance for color detection
        if dominance < self.COLOR_DOMINANCE_FACTOR:
            return "Gray", base_confidence * 0.7
        
        # Determine which color is dominant
        if r_ratio == max_ratio:
            # Red is dominant
            if g_ratio > b_ratio * 1.5 and g_ratio > 60:  # Significant green component
                color = "Orange"
                confidence = base_confidence * min(1.0, (g_ratio / r_ratio) * 2)
            else:
                color = "Red"
                confidence = base_confidence * min(1.0, dominance / 2)
                
        elif g_ratio == max_ratio:
            # Green is dominant
            color = "Green"
            confidence = base_confidence * min(1.0, dominance / 2)
            
        elif b_ratio == max_ratio:
            # Blue is dominant
            if r_ratio > 0.7 * b_ratio:  # Significant red component
                color = "Purple"
                confidence = base_confidence * min(1.0, (r_ratio / b_ratio) * 1.5)
            else:
                color = "Blue"
                confidence = base_confidence * min(1.0, dominance / 2)
        else:
            color = "Unknown"
            confidence = 0.3
        
        # Special case for Yellow (high red and green, low blue)
        if (r_ratio > 100 and g_ratio > 100 and 
            abs(r_ratio - g_ratio) < 50 and 
            b_ratio < max(r_ratio, g_ratio) * 0.7):
            color = "Yellow"
            confidence = base_confidence * 0.9
        
        return color, confidence
    
    def get_normalized_values(self):
        """
        Get the normalized color values (0-255 scale).
        Returns:
            tuple: (r_ratio, g_ratio, b_ratio, clear)
        """
        r, g, b, c = self.get_raw_data()
        if c == 0:
            return 0, 0, 0, 0
            
        r_ratio = (r / c) * 255
        g_ratio = (g / c) * 255
        b_ratio = (b / c) * 255
        
        return r_ratio, g_ratio, b_ratio, c
    
    def calibrate_white(self, samples=10):
        """
        Calibrate white detection by sampling a white surface.
        Place sensor over white surface and call this method.
        
        Args:
            samples: Number of samples to average
            
        Returns:
            dict: Calibration data
        """
        print("Calibrating white... place sensor over white surface")
        time.sleep(2)
        
        clear_values = []
        ratio_spreads = []
        
        for i in range(samples):
            r, g, b, c = self.get_raw_data()
            if c > 0:
                r_ratio = (r / c) * 255
                g_ratio = (g / c) * 255
                b_ratio = (b / c) * 255
                
                ratio_spread = max(r_ratio, g_ratio, b_ratio) - min(r_ratio, g_ratio, b_ratio)
                
                clear_values.append(c)
                ratio_spreads.append(ratio_spread)
                
            time.sleep(0.1)
        
        if clear_values:
            avg_clear = sum(clear_values) / len(clear_values)
            avg_spread = sum(ratio_spreads) / len(ratio_spreads)
            
            # Update thresholds based on calibration
            self.WHITE_MIN_CLEAR = max(1000, avg_clear * 0.7)
            self.WHITE_MAX_RATIO_SPREAD = max(15, avg_spread * 1.5)
            
            calibration_data = {
                'white_min_clear': self.WHITE_MIN_CLEAR,
                'white_max_ratio_spread': self.WHITE_MAX_RATIO_SPREAD,
                'measured_clear': avg_clear,
                'measured_spread': avg_spread
            }
            
            print(f"White calibration complete:")
            print(f"  Clear threshold: {self.WHITE_MIN_CLEAR:.0f}")
            print(f"  Ratio spread threshold: {self.WHITE_MAX_RATIO_SPREAD:.1f}")
            
            return calibration_data
        else:
            print("Calibration failed - no valid readings")
            return None
    
    def set_sensitivity(self, integration_time=0xEB, gain=0x01):
        """
        Adjust sensor sensitivity by changing integration time and gain.
        
        Args:
            integration_time: 0xFF (2.4ms) to 0x00 (614ms), lower = longer integration
            gain: 0x00 (1x), 0x01 (4x), 0x02 (16x), 0x03 (60x)
        """
        self.i2c.writeto_mem(self._ADDR, self._COMMAND_BIT | self._ATIME, bytes([integration_time]))
        self.i2c.writeto_mem(self._ADDR, self._COMMAND_BIT | self._CONTROL, bytes([gain]))
        time.sleep(0.05)
    
    def get_detailed_analysis(self):
        """
        Get detailed color analysis including raw values, ratios, and metrics.
        Useful for debugging and fine-tuning.
        
        Returns:
            dict: Comprehensive color analysis
        """
        color, confidence, (r, g, b, c) = self.get_color()
        r_ratio, g_ratio, b_ratio, _ = self.get_normalized_values()
        
        analysis = {
            'detected_color': color,
            'confidence': confidence,
            'raw_values': {'r': r, 'g': g, 'b': b, 'clear': c},
            'normalized_ratios': {'r': r_ratio, 'g': g_ratio, 'b': b_ratio},
            'metrics': {
                'ratio_spread': max(r_ratio, g_ratio, b_ratio) - min(r_ratio, g_ratio, b_ratio),
                'brightness': c,
                'dominant_channel': ['red', 'green', 'blue'][
                    [r_ratio, g_ratio, b_ratio].index(max(r_ratio, g_ratio, b_ratio))
                ] if c > 0 else 'none'
            }
        }
        
        return analysis