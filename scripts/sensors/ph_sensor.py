"""
Analog pH Meter Sensor Driver for ESP32
Compatible with Analog pH Meter V4.0

Features:
- 0-14 pH range
- 0-3.3V analog output (linear)
- Calibration support
- Dummy data generation when sensor not available
"""

from machine import ADC, Pin
import time
import random

class PHSensor:
    def __init__(self, pin, voltage_calibration=2.5, enable_dummy=True):
        """
        Initialize pH sensor
        
        Args:
            pin: ADC pin number
            voltage_calibration: Bias voltage for calibration (default 2.5V)
            enable_dummy: Generate dummy data if sensor not available (default True)
        """
        self.pin_num = pin
        self.enable_dummy = enable_dummy
        self.ph_value = None
        self._available = False
        
        try:
            self.adc = ADC(Pin(pin))
            self.adc.atten(ADC.ATTN_11DB)  # 0-3.3V range
            self.adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)
            self.voltage_calibration = voltage_calibration
            self._available = True
            print(f'[pH] Sensor initialized on pin {pin}')
        except Exception as e:
            print(f'[pH] Error initializing: {e}')
            self._available = False
        
        # Calibration coefficients (default: linear approximation)
        # Can be adjusted based on calibration with pH 4.01 and 7.00 buffer solutions
        self.slope = 3.5
        self.offset = voltage_calibration
    
    def _generate_dummy_ph(self):
        """Generate realistic dummy pH data for aquaponics"""
        # Ideal aquaponics pH: 6.5-7.5 with slight variations
        base_ph = 7.0
        variation = random.uniform(-0.5, 0.5)
        dummy_ph = round(base_ph + variation, 2)
        print(f'[pH] Generated dummy pH: {dummy_ph}')
        return dummy_ph
    
    def read_voltage(self):
        """
        Read voltage from ADC
        
        Returns:
            Voltage in volts (0-3.3V)
        """
        try:
            adc_value = self.adc.read()
            voltage = (adc_value / 4095.0) * 3.3
            return voltage
        except Exception as e:
            print(f'[pH] Error reading voltage: {e}')
            return None
    
    def read_ph(self, samples=10):
        """
        Read pH value from sensor
        
        Args:
            samples: Number of samples to average (default 10)
            
        Returns:
            pH value (0-14), real or dummy
        """
        # If sensor not available, return dummy data
        if not self._available:
            if self.enable_dummy:
                self.ph_value = self._generate_dummy_ph()
                return self.ph_value
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
                print('[pH] No valid voltage readings')
                if self.enable_dummy:
                    self.ph_value = self._generate_dummy_ph()
                    return self.ph_value
                return None
            
            avg_voltage = voltage_sum / valid_samples
            
            # Check if voltage is within valid range (indicates sensor connected)
            # A disconnected sensor typically reads near 0V or 3.3V
            if avg_voltage < 0.1 or avg_voltage > 3.2:
                print(f'[pH] Voltage out of range ({avg_voltage:.2f}V), sensor may be disconnected')
                if self.enable_dummy:
                    self.ph_value = self._generate_dummy_ph()
                    return self.ph_value
            
            # Convert voltage to pH using linear formula
            # pH = slope * voltage + offset
            ph = self.slope * avg_voltage + self.offset
            
            # Clamp pH to valid range (0-14)
            ph = max(0.0, min(14.0, ph))
            
            self.ph_value = round(ph, 2)
            return self.ph_value
            
        except Exception as e:
            print(f'[pH] Error reading pH: {e}')
            if self.enable_dummy:
                self.ph_value = self._generate_dummy_ph()
                return self.ph_value
            return None
    
    def calibrate(self, buffer_ph, measured_voltage):
        """
        Calibrate pH sensor using buffer solution
        
        Args:
            buffer_ph: pH value of buffer solution (e.g., 4.01, 7.00)
            measured_voltage: Voltage measured when sensor is in buffer
        """
        # For two-point calibration, you need to call this twice
        # with different buffer solutions (pH 4.01 and pH 7.00)
        # Then calculate slope and offset
        
        # Simple one-point calibration (adjusts offset only)
        self.offset = buffer_ph - (self.slope * measured_voltage)
        print(f'[pH] Calibrated: slope={self.slope}, offset={self.offset}')
    
    def set_calibration(self, slope, offset):
        """
        Set calibration coefficients directly
        
        Args:
            slope: Slope coefficient
            offset: Offset coefficient
        """
        self.slope = slope
        self.offset = offset
        print(f'[pH] Calibration set: slope={slope}, offset={offset}')
    
    def get_last_reading(self):
        """Get the last successful pH reading"""
        return self.ph_value
    
    def is_available(self):
        """
        Check if physical sensor is available on the pin
        Tests by reading voltage and checking if it's in valid range
        """
        try:
            voltage = self.read_voltage()
            if voltage is not None and 0.1 <= voltage <= 3.2:
                self._available = True
            else:
                self._available = False
        except:
            self._available = False
        return self._available
