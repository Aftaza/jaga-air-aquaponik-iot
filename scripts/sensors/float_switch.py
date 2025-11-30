"""
Float Switch Sensor Driver for ESP32
Water level detection using normally closed (NC) float switch

Features:
- Digital input (active LOW when water level is low)
- Debouncing logic
- Contact rating: 10W max
"""

from machine import Pin
import time

class FloatSwitch:
    def __init__(self, pin, debounce_ms=50):
        """
        Initialize float switch sensor
        
        Args:
            pin: GPIO pin number
            debounce_ms: Debounce time in milliseconds (default 50ms)
        """
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self.water_level = None
        self.last_state = None
        self.last_change_time = 0
    
    def read_raw(self):
        """
        Read raw pin state
        
        Returns:
            Pin state (0 or 1)
        """
        return self.pin.value()
    
    def is_water_level_normal(self):
        """
        Check if water level is normal (debounced)
        
        Float switch is Normally Closed (NC):
        - HIGH (1): Water level is normal
        - LOW (0): Water level is low
        
        Returns:
            True if water level is normal, False if low
        """
        try:
            current_state = self.pin.value()
            current_time = time.ticks_ms()
            
            # Check if state has changed
            if current_state != self.last_state:
                # Reset debounce timer
                self.last_change_time = current_time
                self.last_state = current_state
            
            # Check if debounce period has passed
            if time.ticks_diff(current_time, self.last_change_time) >= self.debounce_ms:
                # State is stable
                # NC switch: HIGH = normal, LOW = low water level
                self.water_level = bool(current_state)
                return self.water_level
            
            # Return last known stable state
            return self.water_level if self.water_level is not None else True
            
        except Exception as e:
            print(f'[FloatSwitch] Error reading: {e}')
            return True  # Assume normal on error (fail-safe)
    
    def is_water_level_low(self):
        """
        Check if water level is low
        
        Returns:
            True if water level is low, False if normal
        """
        return not self.is_water_level_normal()
    
    def get_last_reading(self):
        """Get the last successful water level reading"""
        return self.water_level
