# ESP32 Setup Guide

## Prerequisites

- ESP32 DevKit V1
- USB cable (micro-USB)
- Computer dengan Python 3
- esptool & ampy (untuk flash & upload)

## 1. Install MicroPython

### Download Firmware

Download MicroPython firmware untuk ESP32:
https://micropython.org/download/esp32/

Pilih versi stable terbaru (e.g., `esp32-20240222-v1.22.2.bin`)

### Flash MicroPython

```bash
# Install esptool
pip install esptool

# Erase flash (optional but recommended)
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# Flash MicroPython
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20240222-v1.22.2.bin
```

**Port Notes:**
- Linux/Mac: `/dev/ttyUSB0` atau `/dev/ttyACM0`
- Windows: `COM3`, `COM4`, dll.

### Verify Installation

```bash
# Install ampy
pip install adafruit-ampy

# Test connection
screen /dev/ttyUSB0 115200
# atau
picocom /dev/ttyUSB0 -b115200
```

Di REPL, ketik:
```python
>>> import sys
>>> sys.implementation
```

Harus menampilkan versi MicroPython.

## 2. Configure Settings

Edit `scripts/config.py`:

```python
# WiFi Settings
WIFI_SSID = 'YourWiFiName'
WIFI_PASSWORD = 'YourWiFiPassword'

# ThingSpeak MQTT Configuration with TLS/SSL
THINGSPEAK_MQTT_BROKER = 'mqtt3.thingspeak.com'
THINGSPEAK_MQTT_PORT = 8883  # TLS/SSL port (use 1883 for non-SSL)
THINGSPEAK_USE_SSL = True    # Enable TLS/SSL encryption
THINGSPEAK_CHANNEL_ID = '1234567'  # Your channel ID
THINGSPEAK_WRITE_API_KEY = 'YOUR_WRITE_API_KEY'
THINGSPEAK_MQTT_USERNAME = 'YOUR_MQTT_USERNAME'
THINGSPEAK_MQTT_PASSWORD = 'YOUR_MQTT_API_KEY'
```

**Security Notes:**
- **TLS/SSL Enabled**: Sistem sekarang menggunakan koneksi MQTT terenkripsi (port 8883)
- **Secure Communication**: Semua data sensor dikirim melalui koneksi terenkripsi TLS/SSL
- **Certificate Validation**: MicroPython akan memvalidasi sertifikat server untuk keamanan maksimal
- **Fallback Option**: Jika mengalami masalah dengan SSL, ubah `THINGSPEAK_USE_SSL = False` dan `THINGSPEAK_MQTT_PORT = 1883`

Lihat [THINGSPEAK_SETUP.md](THINGSPEAK_SETUP.md) untuk mendapatkan credentials.

## 3. Upload Code to ESP32

### Method 1: Using ampy

```bash
cd scripts

# Upload files satu per satu
ampy --port /dev/ttyUSB0 put config.py
ampy --port /dev/ttyUSB0 put wifi_manager.py
ampy --port /dev/ttyUSB0 put mqtt_client.py
ampy --port /dev/ttyUSB0 put boot.py
ampy --port /dev/ttyUSB0 put main.py

# Upload folders
ampy --port /dev/ttyUSB0 put sensors sensors
ampy --port /dev/ttyUSB0 put actuators actuators
```

### Method 2: Using rshell

```bash
# Install rshell
pip install rshell

# Connect
rshell --port /dev/ttyUSB0

# Copy files
/home/your-name> cp config.py /pyboard/
/home/your-name> cp *.py /pyboard/
/home/your-name> cp -r sensors /pyboard/
/home/your-name> cp -r actuators /pyboard/
```

### Method 3: Using Thonny IDE

1. Install Thonny: https://thonny.org/
2. Tools → Options → Interpreter
3. Select "MicroPython (ESP32)"
4. Upload files via file manager

## 4. Wiring Diagram

### Sensors

| Sensor | ESP32 Pin | Connection |
|--------|-----------|------------|
| DS18B20 | GPIO 25 | Data (OneWire) |
| DS18B20 | 3.3V | VCC |
| DS18B20 | GND | GND |
| DS18B20 | GPIO 25 & 3.3V | 4.7kΩ pull-up resistor |
| pH Sensor | GPIO 34 (ADC1_CH6) | Signal |
| pH Sensor | 5V | VCC |
| pH Sensor | GND | GND |
| TDS Sensor | GPIO 32 (ADC1_CH4) | Signal |
| TDS Sensor | 3.3V | VCC |
| TDS Sensor | GND | GND |
| Float Switch | GPIO 27 | Signal |
| Float Switch | GND | GND (NC contact) |

### Actuators

| Actuator | ESP32 Pin | Connection |
|----------|-----------|------------|
| Relay Module VCC | 5V | Power |
| Relay Module GND | GND | Ground |
| Relay Pump IN | GPIO 16 | Signal |
| Relay Light IN | GPIO 17 | Signal |

### Power Supply

- ESP32: 5V via USB atau VIN pin
- Relay Module: 5V 3A (shared dengan ESP32)
- Sensors: 3.3V/5V dari ESP32

⚠️ **Important**: Gunakan power supply yang cukup (min 2-3A) untuk ESP32 + relay + sensors.

## 5. First Boot

```bash
# Open serial monitor
screen /dev/ttyUSB0 115200
```

Reset ESP32 (tekan tombol EN/RST).

Output yang diharapkan:
```
==================================================
IoT Aquaponik Mini - ESP32
Firmware Version: 1.0.0
==================================================

[Boot] Configuration loaded
[Boot] Free memory: 110000 bytes
[Boot] Boot completed, starting main application...

[System] Initializing...
[DS18B20] Found 1 device(s)
[Relay] Initialized
[WiFi] Connecting to YourWiFi...
[WiFi] Connected successfully
[MQTT] Client initialized
  Broker: mqtt3.thingspeak.com:8883
  SSL/TLS: Enabled
  Channel: 1234567
[MQTT] Connecting to broker...
[MQTT] Using SSL/TLS encryption
[MQTT] Connected successfully
[System] Starting main loop...
```

## 6. Testing

### Test Sensors

```python
# Di REPL
>>> from sensors.ds18b20 import DS18B20Sensor
>>> temp = DS18B20Sensor(25)
>>> temp.read_temperature()
26.5
```

### Test Relay

```python
>>> from actuators.relay import RelayController
>>> relay = RelayController(16, 17)
>>> relay.set_pump(True)   # Turn ON pump
>>> relay.set_pump(False)  # Turn OFF pump
```

## Troubleshooting

### Cannot Connect to ESP32

- Check USB cable (must support data transfer)
- Try different USB port
- Install CH340/CP2102 drivers if needed
- Check port dengan `ls /dev/tty*`

### MicroPython Not Responding

- Re-flash MicroPython firmware
- Try different firmware version
- Check ESP32 with blink example

### File Upload Fails

- Check available space: `import os; os.stat('/')`
- Erase flash dan re-upload
- Try different upload method

### Sensors Not Reading

- Check wiring connections
- Verify pin numbers dalam config.py
- Test sensors individually di REPL

### SSL/TLS Connection Issues

**Error: "SSL handshake failed" atau "Connection timeout"**

1. **Verify SSL is enabled in config.py:**
   ```python
   THINGSPEAK_USE_SSL = True
   THINGSPEAK_MQTT_PORT = 8883
   ```

2. **Check MicroPython SSL support:**
   ```python
   >>> import ussl
   >>> # If no error, SSL is supported
   ```

3. **Verify time is set correctly** (required for certificate validation):
   ```python
   >>> import time
   >>> time.localtime()
   # Should show current time, not 2000-01-01
   ```

4. **Test with non-SSL first** (untuk debugging):
   ```python
   THINGSPEAK_USE_SSL = False
   THINGSPEAK_MQTT_PORT = 1883
   ```

5. **Memory issues**: SSL requires more memory, pastikan free memory > 50KB:
   ```python
   >>> import gc
   >>> gc.collect()
   >>> gc.mem_free()
   ```

6. **Update MicroPython firmware**: Gunakan versi terbaru yang support SSL/TLS

**Error: "MQTT Connection refused"**

- Verify MQTT credentials (username/password)
- Check ThingSpeak channel ID
- Ensure MQTT is enabled di ThingSpeak channel settings
- Check firewall tidak memblokir port 8883

## Additional Resources

- MicroPython ESP32 Quick Reference: https://docs.micropython.org/en/latest/esp32/quickref.html
- ESP32 Pinout: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
