"""
2-Channel Relay Module Driver for ESP32
Control water pump and grow light

Features:
- Active LOW trigger (relay activates when pin is LOW)
- 10A 250VAC / 10A 30VDC rating
- Separate control for pump and light
"""

from machine import Pin

class RelayController:
    def __init__(self, pump_pin, light_pin):
        """
        Initialize relay controller
        
        Args:
            pump_pin: GPIO pin for pump relay
            light_pin: GPIO pin for light relay
        """
        # Initialize pins as outputs, start with relays OFF (HIGH = OFF for active LOW)
        self.pump_pin = Pin(pump_pin, Pin.OUT, value=1)
        self.light_pin = Pin(light_pin, Pin.OUT, value=1)
        
        self.pump_status = False
        self.light_status = False
        
        print('[Relay] Initialized')
        print(f'  Pump relay: GPIO {pump_pin}')
        print(f'  Light relay: GPIO {light_pin}')
    
    def set_pump(self, state):
        """
        Control pump relay
        
        Args:
            state: True to turn ON, False to turn OFF
        """
        try:
            # Active LOW: LOW (0) = ON, HIGH (1) = OFF
            self.pump_pin.value(0 if state else 1)
            self.pump_status = state
            print(f'[Relay] Pump: {"ON" if state else "OFF"}')
            return True
        except Exception as e:
            print(f'[Relay] Error controlling pump: {e}')
            return False
    
    def set_light(self, state):
        """
        Control light relay
        
        Args:
            state: True to turn ON, False to turn OFF
        """
        try:
            # Active LOW: LOW (0) = ON, HIGH (1) = OFF
            self.light_pin.value(0 if state else 1)
            self.light_status = state
            print(f'[Relay] Light: {"ON" if state else "OFF"}')
            return True
        except Exception as e:
            print(f'[Relay] Error controlling light: {e}')
            return False
    
    def get_pump_status(self):
        """Get current pump status"""
        return self.pump_status
    
    def get_light_status(self):
        """Get current light status"""
        return self.light_status
    
    def turn_all_off(self):
        """Turn off all relays (emergency stop)"""
        try:
            self.set_pump(False)
            self.set_light(False)
            print('[Relay] All relays turned OFF')
            return True
        except Exception as e:
            print(f'[Relay] Error turning off all relays: {e}')
            return False
    
    def get_status(self):
        """
        Get status of both relays
        
        Returns:
            Dictionary with pump and light status
        """
        return {
            'pump': self.pump_status,
            'light': self.light_status
        }
