# Sensor Calibration Guide

## pH Sensor Calibration

### Required Materials
- pH 4.01 buffer solution
- pH 7.00 buffer solution (optional: pH 10.01)
- Distilled water untuk bilas
- Soft tissue untuk mengeringkan probe

### Calibration Steps

1. **Warm Up**
   ```python
   # Hubungkan pH sensor ke ESP32
   # Tunggu 5-10 menit untuk warm-up
   ```

2. **Read Raw Voltage**
   ```python
   from sensors.ph_sensor import PHSensor
   ph = PHSensor(34)
   
   # Celupkan probe ke pH 7.00 buffer
   voltage_ph7 = ph.read_voltage()
   print(f"pH 7.00 voltage: {voltage_ph7}V")
   
   # Bilas dengan distilled water
   # Celupkan probe ke pH 4.01 buffer
   voltage_ph4 = ph.read_voltage()
   print(f"pH 4.01 voltage: {voltage_ph4}V")
   ```

3. **Calculate Calibration**
   ```python
   # Two-point calibration
   # slope = (pH2 - pH1) / (V2 - V1)
   slope = (7.0 - 4.01) / (voltage_ph7 - voltage_ph4)
   
   # offset = pH1 - (slope * V1)
   offset = 4.01 - (slope * voltage_ph4)
   
   print(f"Slope: {slope}")
   print(f"Offset: {offset}")
   ```

4. **Set Calibration**
   ```python
   ph.set_calibration(slope, offset)
   ```

5. **Update config.py**
   ```python
   # Edit scripts/config.py
   PH_SLOPE = 3.2  # Your calculated slope
   PH_OFFSET = 2.1  # Your calculated offset
   ```

6. **Verify Calibration**
   ```python
   # Test dengan buffer solution
   ph_value = ph.read_ph()
   print(f"pH reading: {ph_value}")
   # Harus close to 4.01 atau 7.00
   ```

### Typical Values

- **Slope**: 3.0 - 3.5
- **Offset**: 2.0 - 3.0
- **Voltage at pH 7**: ~2.5V

### Maintenance

- Calibrate setiap minggu untuk akurasi optimal
- Store probe dalam pH 4.01 storage solution
- Jangan biarkan probe kering
- Replace probe setiap 6-12 bulan

## TDS Sensor Calibration

### Required Materials
- TDS calibration solution (342 ppm atau 1413 μS/cm)
- Distilled water (0 ppm)
- Thermometer

### Calibration Steps

1. **Zero Point (Optional)**
   ```python
   from sensors.tds_sensor import TDSSensor
   tds = TDSSensor(32)
   
   # Celupkan probe ke distilled water
   voltage_zero = tds.read_voltage()
   print(f"Zero voltage: {voltage_zero}V")
   # Should be very close to 0V
   ```

2. **Calibration Point**
   ```python
   # Celupkan probe ke 342 ppm solution
   # Ukur suhu solution
   temp = 25.0  # °C
   
   # Read raw TDS
   tds_value = tds.read_tds(temperature=temp)
   print(f"TDS reading: {tds_value} ppm")
   ```

3. **Calculate Correction Factor**
   ```python
   # Expected: 342 ppm
   # Actual: tds_value ppm
   correction_factor = 342 / tds_value
   print(f"Correction factor: {correction_factor}")
   ```

4. **Apply Correction**
   
   Edit `scripts/sensors/tds_sensor.py`:
   ```python
   # Line ~55, setelah polynomial calculation
   tds = tds * correction_factor  # Add this line
   ```

### Temperature Compensation

TDS sensor sudah include temperature compensation dalam code:

```python
compensation_coefficient = 1.0 + 0.02 * (temperature - 25.0)
```

- Base reference: 25°C
- Coefficient: 0.02 per degree

### Verification

Test dengan beberapa TDS solution:
- 0 ppm (distilled water): ~0-10 ppm
- 342 ppm: 330-355 ppm
- 1000 ppm: 950-1050 ppm

## Temperature Sensor (DS18B20)

DS18B20 adalah factory-calibrated sensor, tidak memerlukan calibration manual.

### Verification

```python
from sensors.ds18b20 import DS18B20Sensor
temp = DS18B20Sensor(25)

# Compare dengan thermometer reference
reading = temp.read_temperature()
print(f"Temperature: {reading}°C")
```

### Accuracy

- ±0.5°C (0-50°C range)
- ±2°C (-55 to +125°C full range)

### Troubleshooting

Jika reading tidak akurat:
1. Check wiring (especially pull-up resistor 4.7kΩ)
2. Verify power supply is stable
3. Try different DS18B20 (sensor might be defective)

## Float Switch

Float switch adalah digital ON/OFF sensor, tidak memerlukan calibration.

### Testing

```python
from sensors.float_switch import FloatSwitch
switch = FloatSwitch(27)

print(f"Water level normal: {switch.is_water_level_normal()}")
print(f"Water level low: {switch.is_water_level_low()}")
```

Physically raise/lower float untuk verify:
- Float UP (normal water level): `True`
- Float DOWN (low water level): `False`

## Calibration Schedule

| Sensor | Frequency | Notes |
|--------|-----------|-------|
| pH Meter | Weekly | Critical for accuracy |
| TDS Sensor | Monthly | Less critical |
| DS18B20 | N/A | Factory calibrated |
| Float Switch | N/A | Mechanical, no calibration needed |

## Best Practices

1. **Environment**
   - Calibrate di suhu ruangan (20-25°C)
   - Avoid extreme temperatures saat calibration

2. **Solutions**
   - Use fresh buffer/calibration solutions
   - Store solutions properly (sealed, cool)
   - Check expiration dates

3. **Probe Care**
   - Always rinse dengan distilled water sebelum/sesudah calibration
   - Dry gently dengan soft tissue
   - Avoid touching probe tip

4. **Documentation**
   - Record calibration date
   - Save calibration values
   - Track sensor performance over time
