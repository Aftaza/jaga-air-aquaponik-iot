"""
Analog TDS Sensor Driver for ESP32
Total Dissolved Solids (TDS) measurement with temperature compensation

Features:
- 0-1000 ppm range
- Temperature compensation
- ±10% F.S. accuracy
"""

from machine import ADC, Pin
import time

class TDSSensor:
    def __init__(self, pin, vref=3.3):
        """
        Initialize TDS sensor
        
        Args:
            pin: ADC pin number
            vref: Reference voltage (default 3.3V for ESP32)
        """
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)  # 0-3.3V range
        self.adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)
        self.vref = vref
        self.tds_value = None
    
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
            TDS value in ppm, or None if error
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
                print('[TDS] No valid voltage readings')
                return None
            
            avg_voltage = voltage_sum / valid_samples
            
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
            return None
    
    def get_last_reading(self):
        """Get the last successful TDS reading"""
        return self.tds_value
