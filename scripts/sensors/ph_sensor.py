"""
Analog pH Meter Sensor Driver for ESP32
Compatible with Analog pH Meter V4.0

Features:
- 0-14 pH range
- 0-3.3V analog output (linear)
- Calibration support
"""

from machine import ADC, Pin
import time

class PHSensor:
    def __init__(self, pin, voltage_calibration=2.5):
        """
        Initialize pH sensor
        
        Args:
            pin: ADC pin number
            voltage_calibration: Bias voltage for calibration (default 2.5V)
        """
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)  # 0-3.3V range
        self.adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)
        self.voltage_calibration = voltage_calibration
        self.ph_value = None
        
        # Calibration coefficients (default: linear approximation)
        # Can be adjusted based on calibration with pH 4.01 and 7.00 buffer solutions
        self.slope = 3.5
        self.offset = voltage_calibration
    
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
            pH value (0-14), or None if error
        """
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
                return None
            
            avg_voltage = voltage_sum / valid_samples
            
            # Convert voltage to pH using linear formula
            # pH = slope * voltage + offset
            ph = self.slope * avg_voltage + self.offset
            
            # Clamp pH to valid range (0-14)
            ph = max(0.0, min(14.0, ph))
            
            self.ph_value = round(ph, 2)
            return self.ph_value
            
        except Exception as e:
            print(f'[pH] Error reading pH: {e}')
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
