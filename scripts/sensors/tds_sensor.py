"""
Analog TDS Sensor Driver for ESP32
Total Dissolved Solids (TDS) measurement with temperature compensation

Features:
- 0-1000 ppm range
- Temperature compensation
- ±10% F.S. accuracy
- Dummy data generation when sensor not available
"""

from machine import ADC, Pin
import time
import random

class TDSSensor:
    def __init__(self, pin, vref=3.3, enable_dummy=True):
        """
        Initialize TDS sensor
        
        Args:
            pin: ADC pin number
            vref: Reference voltage (default 3.3V for ESP32)
            enable_dummy: Generate dummy data if sensor not available (default True)
        """
        self.pin_num = pin
        self.vref = vref
        self.enable_dummy = enable_dummy
        self.tds_value = None
        self._available = False
        
        try:
            self.adc = ADC(Pin(pin))
            self.adc.atten(ADC.ATTN_11DB)  # 0-3.3V range
            self.adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)
            self._available = True
            print(f'[TDS] Sensor initialized on pin {pin}')
        except Exception as e:
            print(f'[TDS] Error initializing: {e}')
            self._available = False
    
    def _generate_dummy_tds(self):
        """Generate realistic dummy TDS data for aquaponics"""
        # Ideal aquaponics TDS: 300-600 ppm with variations
        base_tds = 450
        variation = random.randint(-100, 100)
        dummy_tds = max(200, min(800, base_tds + variation))
        print(f'[TDS] Generated dummy TDS: {dummy_tds} ppm')
        return dummy_tds
    
    def read_voltage(self):
        """
        Read voltage from ADC
        
        Returns:
            Voltage in volts (0-3.3V)
        """
        try:
            adc_value = self.adc.read()
            voltage = (adc_value / 4095.0) * self.vref
            return voltage
        except Exception as e:
            print(f'[TDS] Error reading voltage: {e}')
            return None
    
    def read_tds(self, temperature=25.0, samples=10):
        """
        Read TDS value from sensor with temperature compensation
        
        Args:
            temperature: Water temperature in Celsius (for compensation)
            samples: Number of samples to average (default 10)
            
        Returns:
            TDS value in ppm (real or dummy)
        """
        # If sensor not available, return dummy data
        if not self._available:
            if self.enable_dummy:
                self.tds_value = self._generate_dummy_tds()
                return self.tds_value
            return None
        
        try:
            # Take multiple samples and average
            voltage_sum = 0
            valid_samples = 0
            
            for i in range(samples):
                voltage = self.read_voltage()
                if voltage is not None:
                    voltage_sum += voltage
                    valid_samples += 1
                time.sleep_ms(10)
            
            if valid_samples == 0:
                print('[TDS] No valid voltage readings')
                if self.enable_dummy:
                    self.tds_value = self._generate_dummy_tds()
                    return self.tds_value
                return None
            
            avg_voltage = voltage_sum / valid_samples
            
            # Check if voltage is within valid range (indicates sensor connected)
            # A disconnected sensor typically reads near 0V or 3.3V
            if avg_voltage < 0.05 or avg_voltage > 3.2:
                print(f'[TDS] Voltage out of range ({avg_voltage:.2f}V), sensor may be disconnected')
                if self.enable_dummy:
                    self.tds_value = self._generate_dummy_tds()
                    return self.tds_value
            
            # Temperature compensation
            # Compensation coefficient: 0.02 per degree from 25°C
            compensation_coefficient = 1.0 + 0.02 * (temperature - 25.0)
            compensated_voltage = avg_voltage / compensation_coefficient
            
            # Convert voltage to TDS using polynomial formula
            # TDS (ppm) = (133.42*V^3 - 255.86*V^2 + 857.39*V) * 0.5
            tds = (133.42 * (compensated_voltage ** 3) 
                   - 255.86 * (compensated_voltage ** 2) 
                   + 857.39 * compensated_voltage) * 0.5
            
            # Clamp TDS to valid range (0-1000 ppm)
            tds = max(0, min(1000, int(tds)))
            
            self.tds_value = tds
            return self.tds_value
            
        except Exception as e:
            print(f'[TDS] Error reading TDS: {e}')
            if self.enable_dummy:
                self.tds_value = self._generate_dummy_tds()
                return self.tds_value
            return None
    
    def get_last_reading(self):
        """Get the last successful TDS reading"""
        return self.tds_value
    
    def is_available(self):
        """
        Check if physical sensor is available on the pin
        Tests by reading voltage and checking if it's in valid range
        """
        try:
            voltage = self.read_voltage()
            if voltage is not None and 0.05 <= voltage <= 3.2:
                self._available = True
            else:
                self._available = False
        except:
            self._available = False
        return self._available
