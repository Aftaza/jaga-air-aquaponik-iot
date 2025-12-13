"""
DS18B20 OneWire Temperature Sensor Driver for ESP32
Based on Dallas/Maxim DS18B20 digital thermometer

Features:
- 9-12 bit resolution (configurable)
- -55°C to +125°C range
- ±0.5°C accuracy (0-50°C)
- Dummy data generation when sensor not available
"""

import time
import random
from machine import Pin
import onewire
import ds18x20

class DS18B20Sensor:
    def __init__(self, pin, enable_dummy=True):
        """
        Initialize DS18B20 sensor on OneWire bus
        
        Args:
            pin: GPIO pin number for OneWire data line
            enable_dummy: Generate dummy data if sensor not available (default True)
        """
        self.pin_num = pin
        self.enable_dummy = enable_dummy
        self.devices = []
        self.temp = None
        self._available = False
        
        try:
            self.pin = Pin(pin)
            self.ow = onewire.OneWire(self.pin)
            self.ds = ds18x20.DS18X20(self.ow)
            # Scan for devices on the bus
            self._scan_devices()
        except Exception as e:
            print(f'[DS18B20] Error initializing: {e}')
            self._available = False
    
    def _scan_devices(self):
        """Scan for DS18B20 devices on the OneWire bus"""
        try:
            self.devices = self.ow.scan()
            if len(self.devices) == 0:
                print('[DS18B20] No devices found on bus')
                self._available = False
            else:
                print(f'[DS18B20] Found {len(self.devices)} device(s)')
                for i, device in enumerate(self.devices):
                    print(f'  Device {i}: {self._rom_to_hex(device)}')
                self._available = True
        except Exception as e:
            print(f'[DS18B20] Error scanning devices: {e}')
            self._available = False
    
    def _rom_to_hex(self, rom):
        """Convert ROM address to hexadecimal string"""
        return ''.join('%02x' % b for b in rom)
    
    def _generate_dummy_temperature(self):
        """Generate realistic dummy temperature data for aquaponics"""
        # Typical aquaponics temperature: 22-28°C with slight variations
        base_temp = 25.0
        variation = random.uniform(-2.5, 2.5)
        dummy_temp = round(base_temp + variation, 2)
        print(f'[DS18B20] Generated dummy temperature: {dummy_temp}°C')
        return dummy_temp
    
    def read_temperature(self, index=0):
        """
        Read temperature from DS18B20 sensor
        
        Args:
            index: Device index (default 0 for first device)
            
        Returns:
            Temperature in Celsius (real or dummy), or None if error and dummy disabled
        """
        # If no sensor available, try to generate dummy data
        if not self._available or len(self.devices) == 0:
            if self.enable_dummy:
                self.temp = self._generate_dummy_temperature()
                return self.temp
            else:
                print('[DS18B20] No devices available')
                return None
        
        if index >= len(self.devices):
            print(f'[DS18B20] Invalid device index: {index}')
            if self.enable_dummy:
                self.temp = self._generate_dummy_temperature()
                return self.temp
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
                if self.enable_dummy:
                    self.temp = self._generate_dummy_temperature()
                    return self.temp
                return None
                
        except Exception as e:
            print(f'[DS18B20] Error reading temperature: {e}')
            if self.enable_dummy:
                self.temp = self._generate_dummy_temperature()
                return self.temp
            return None
    
    def get_last_reading(self):
        """Get the last successful temperature reading"""
        return self.temp
    
    def is_available(self):
        """Check if physical sensor is available on the pin"""
        # Re-scan to check current availability
        try:
            self.devices = self.ow.scan()
            self._available = len(self.devices) > 0
        except:
            self._available = False
        return self._available
    
    def rescan(self):
        """Rescan for devices on the bus"""
        self._scan_devices()
        return self._available
