"""
DS18B20 OneWire Temperature Sensor Driver for ESP32
Based on Dallas/Maxim DS18B20 digital thermometer

Features:
- 9-12 bit resolution (configurable)
- -55°C to +125°C range
- ±0.5°C accuracy (0-50°C)
"""

import time
from machine import Pin
import onewire
import ds18x20

class DS18B20Sensor:
    def __init__(self, pin):
        """
        Initialize DS18B20 sensor on OneWire bus
        
        Args:
            pin: GPIO pin number for OneWire data line
        """
        self.pin = Pin(pin)
        self.ow = onewire.OneWire(self.pin)
        self.ds = ds18x20.DS18X20(self.ow)
        self.devices = []
        self.temp = None
        
        # Scan for devices on the bus
        self._scan_devices()
    
    def _scan_devices(self):
        """Scan for DS18B20 devices on the OneWire bus"""
        try:
            self.devices = self.ow.scan()
            if len(self.devices) == 0:
                print('[DS18B20] No devices found on bus')
            else:
                print(f'[DS18B20] Found {len(self.devices)} device(s)')
                for i, device in enumerate(self.devices):
                    print(f'  Device {i}: {self._rom_to_hex(device)}')
        except Exception as e:
            print(f'[DS18B20] Error scanning devices: {e}')
    
    def _rom_to_hex(self, rom):
        """Convert ROM address to hexadecimal string"""
        return ''.join('%02x' % b for b in rom)
    
    def read_temperature(self, index=0):
        """
        Read temperature from DS18B20 sensor
        
        Args:
            index: Device index (default 0 for first device)
            
        Returns:
            Temperature in Celsius, or None if error
        """
        if len(self.devices) == 0:
            print('[DS18B20] No devices available')
            return None
        
        if index >= len(self.devices):
            print(f'[DS18B20] Invalid device index: {index}')
            return None
        
        try:
            # Start temperature conversion
            self.ds.convert_temp()
            
            # Wait for conversion to complete (750ms for 12-bit resolution)
            time.sleep_ms(750)
            
            # Read temperature
            device = self.devices[index]
            temp = self.ds.read_temp(device)
            
            # Validate temperature reading
            if temp is not None and -55 <= temp <= 125:
                self.temp = round(temp, 2)
                return self.temp
            else:
                print(f'[DS18B20] Invalid temperature reading: {temp}')
                return None
                
        except Exception as e:
            print(f'[DS18B20] Error reading temperature: {e}')
            return None
    
    def get_last_reading(self):
        """Get the last successful temperature reading"""
        return self.temp
    
    def is_available(self):
        """Check if sensor is available"""
        return len(self.devices) > 0
