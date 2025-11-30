# Troubleshooting Guide

## Flutter App Issues

### Build Errors

#### Problem: "Gradle build failed"
**Solutions**:
```bash
# Clean project
flutter clean
cd android
./gradlew clean
cd ..

# Update dependencies
flutter pub get

# Rebuild
flutter run
```

#### Problem: "SDK version mismatch"
**Solution**: Edit `android/app/build.gradle`:
```gradle
android {
    compileSdk 34
    defaultConfig {
        minSdk 21
        targetSdk 34
    }
}
```

### Runtime Errors

#### Problem: "Charts not displaying"
**Possible Causes**:
1. Data list is empty
2. Chart dimensions invalid
3. fl_chart version issue

**Solutions**:
- Check mock data service is generating data
- Verify chart widget has proper constraints
- Try `flutter pub upgrade fl_chart`

#### Problem: "App crashes on startup"
**Solutions**:
```bash
# Check logs
flutter logs

# Run in debug mode
flutter run --debug

# Check for null safety issues
```

### UI Issues

#### Problem: "Bottom navigation not switching screens"
**Solution**: Check `HomeScreen` state management:
```dart
setState(() {
  _currentIndex = index;
});
```

## ESP32 Issues

### Connection Problems

#### Problem: "Cannot connect to ESP32"
**Diagnostics**:
```bash
# Check port
ls /dev/tty*

# Linux: Look for /dev/ttyUSB0 or /dev/ttyACM0
# Mac: Look for /dev/cu.usbserial*
# Windows: Check Device Manager for COM port
```

**Solutions**:
1. Install CH340/CP2102 drivers
2. Try different USB cable (must support data)
3. Try different USB port
4. Check ESP32 is powered (LED should light up)

#### Problem: "Permission denied on /dev/ttyUSB0"
**Solution** (Linux):
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Logout and login again, or:
newgrp dialout

# Or use sudo
sudo chmod 666 /dev/ttyUSB0
```

### MicroPython Issues

#### Problem: "Flash failed" or "Erase failed"
**Solutions**:
1. Hold BOOT button while connecting
2. Try slower baud rate:
   ```bash
   esptool.py --baud 115200 write_flash ...
   ```
3. Erase flash first:
   ```bash
   esptool.py erase_flash
   ```

#### Problem: "Import error in REPL"
**Causes**:
- File not uploaded correctly
- Syntax error dalam code
- Memory insufficient

**Solutions**:
```python
# Check uploaded files
import os
os.listdir('/')

# Check available memory
import gc
gc.mem_free()  # Should be > 50000 bytes

# Try import dengan detailed error
try:
    import config
except Exception as e:
    print(e)
```

### WiFi Problems

#### Problem: "WiFi connection timeout"
**Diagnostics**:
```python
from wifi_manager import WiFiManager
wifi = WiFiManager('YourSSID', 'YourPassword')

# Try connect dengan debug
wifi.connect()
# Watch serial output for error messages
```

**Solutions**:
1. Check SSID dan password dalam config.py
2. Ensure WiFi is 2.4GHz (ESP32 tidak support 5GHz)
3. Move ESP32 closer to router
4. Check WiFi credentials tidak ada special characters
5. Try different WiFi network

#### Problem: "WiFi connects then disconnects"
**Solutions**:
1. Check router settings (DHCP enabled)
2. Assign static IP to ESP32
3. Disable router's MAC filtering temporarily
4. Check power supply stability (voltage drops?)

### MQTT Problems

#### Problem: "MQTT connection failed"
**Diagnostics**:
```python
from mqtt_client import ThingSpeakMQTT
import config

mqtt = ThingSpeakMQTT(
    broker=config.THINGSPEAK_MQTT_BROKER,
    port=config.THINGSPEAK_MQTT_PORT,
    username=config.THINGSPEAK_MQTT_USERNAME,
    password=config.THINGSPEAK_MQTT_PASSWORD,
    client_id=config.THINGSPEAK_CLIENT_ID,
    channel_id=config.THINGSPEAK_CHANNEL_ID
)

mqtt.connect()
```

**Solutions**:
1. Verify MQTT credentials di ThingSpeak
2. Check WiFi is connected first
3. Try broker test: `mqtt3.thingspeak.com`
4. Check firewall tidak blocking port 1883
5. Regenerate MQTT API key di ThingSpeak

#### Problem: "Data not appearing on ThingSpeak"
**Diagnostics**:
- Check serial monitor untuk publish success
- Verify field mapping correct (field1, field2, etc.)
- Check ThingSpeak channel configuration

**Solutions**:
1. Wait 30 seconds for data to appear
2. Check update interval (min 15s for HTTP, recommended 60s for MQTT)
3. Verify Write API key correct
4. Check payload format:
   ```python
   # Should be:
   field1=26.5&field2=6.8&field3=450
   ```

### Sensor Problems

#### Problem: "DS18B20 not found"
**Diagnostics**:
```python
from sensors.ds18b20 import DS18B20Sensor
temp = DS18B20Sensor(25)
# Check output: should show "Found X device(s)"
```

**Solutions**:
1. Check wiring (especially pull-up resistor 4.7kΩ)
2. Verify power supply (3.3V)
3. Try different GPIO pin
4. Test sensor dengan multimeter
5. Try different DS18B20 sensor

#### Problem: "pH sensor reading stuck at 0 or random values"
**Solutions**:
1. Check ADC pin connection
2. Verify pH probe dalam water (not air)
3. Calibrate sensor (see SENSOR_CALIBRATION.md)
4. Check pH probe tidak rusak (test dengan multimeter)
5. Wait for sensor warm-up (5-10 minutes)

#### Problem: "TDS sensor reading 0 or 1000"
**Solutions**:
1. Verify TDS probe dalam water
2. Check ADC connection
3. Calibrate dengan TDS solution
4. Test dengan different water sample
5. Check temperature reading (affects TDS)

#### Problem: "Float switch always shows LOW"
**Solutions**:
1. Check wiring (COM to GPIO, NC to GND)
2. Verify float can move freely
3. Test manual dengan multimeter
4. Check code: `Pin.PULL_UP` enabled
5. Try different GPIO pin

### Relay Problems

#### Problem: "Relay not clicking"
**Diagnostics**:
```python
from actuators.relay import RelayController
relay = RelayController(16, 17)

# Test pump
relay.set_pump(True)   # Should hear click
relay.set_pump(False)  # Should hear click

# Check pin output
from machine import Pin
pin = Pin(16, Pin.OUT)
pin.value(0)  # Relay should activate
pin.value(1)  # Relay should deactivate
```

**Solutions**:
1. Check relay power (needs 5V)
2. Verify signal wire connection
3. Check GPIO pin numbers
4. Test relay dengan external power source
5. Relay might be faulty - test dengan LED

#### Problem: "Relay stuck ON or OFF"
**Solutions**:
1. Check Active LOW configuration (0=ON, 1=OFF)
2. Power cycle relay module
3. Check for code errors keeping relay state
4. Replace relay module

### Memory Problems

#### Problem: "MemoryError" or crashes
**Solutions**:
```python
# Check free memory
import gc
gc.mem_free()

# Force garbage collection
gc.collect()

# Reduce update intervals dalam config.py
SENSOR_READ_INTERVAL = 60  # Increase from 30
```

**Tips**:
- Avoid string concatenation dalam loops
- Delete large variables when done
- Use generators instead of lists
- Simplify code logic

### Watchdog Reset

#### Problem: "ESP32 keeps resetting"
**Causes**:
- Code crash/exception
- Watchdog timeout (> 2 minutes dalam loop)
- Power supply issue

**Diagnostics**:
```python
# Disable watchdog temporarily untuk debugging
# Comment out dalam main.py:
# self.wdt = WDT(timeout=...)
```

**Solutions**:
1. Check error messages di serial monitor
2. Add more `wdt.feed()` calls dalam loops
3. Handle exceptions properly
4. Check power supply stability

## ThingSpeak Issues

### API Rate Limit

#### Problem: "Update ignored" or "HTTP 429"
**Solution**: Increase publish interval:
```python
MQTT_PUBLISH_INTERVAL = 60  # Minimum recommended
```

### Channel Issues

#### Problem: "Invalid channel ID"
**Solutions**:
1. Verify channel ID dari URL
2. Check channel tidak deleted
3. Ensure using correct ThingSpeak account

## General Debugging Tips

### Enable Debug Mode

Edit `scripts/config.py`:
```python
DEBUG = True  # Enable verbose output
```

### Serial Monitor

```bash
# Linux/Mac
screen /dev/ttyUSB0 115200

# Or use minicom
minicom -D /dev/ttyUSB0 -b 115200

# To exit screen: Ctrl+A, then K, then Y
```

### Check System Status

```python
# In REPL
import gc
import esp

print('Free memory:', gc.mem_free())
print('Flash size:', esp.flash_size())

import network
wlan = network.WLAN(network.STA_IF)
print('Connected:', wlan.isconnected())
print('IP:', wlan.ifconfig())
```

### Reset Everything

1. **Soft Reset**: Ctrl+D dalam REPL
2. **Hard Reset**: Press EN/RST button
3. **Full Reset**: Re-flash MicroPython
4. **Factory Reset**: Erase flash completely

## Getting Help

### Check Logs

**Flutter**:
```bash
flutter logs
```

**ESP32**:
Serial monitor output

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `OSError: [Errno 113] EHOSTUNREACH` | Network unreachable | Check WiFi connection |
| `OSError: [Errno 104] ECONNRESET` | Connection reset | Check MQTT settings |
| `MemoryError` | Out of memory | Run gc.collect() |
| `AttributeError` | Object/method not found | Check import statements |
| `TypeError` | Wrong data type | Check function arguments |

### Resources

- ESP32 Forum: https://www.esp32.com/
- MicroPython Forum: https://forum.micropython.org/
- Flutter Community: https://flutter.dev/community
- ThingSpeak Support: https://www.mathworks.com/support/

## Preventive Maintenance

1. **Weekly**:
   - Check sensor calibration
   - Verify data accuracy
   - Clean sensors

2. **Monthly**:
   - Check all connections
   - Test relay operation
   - Update firmware if needed
   - Backup configuration

3. **Quarterly**:
   - Deep clean sensors
   - Replace worn components
   - Review threshold settings
   - Performance optimization
