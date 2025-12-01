# ESP32 MicroPython Scripts - SSL/TLS Enabled

## 📁 File Structure

```
scripts/
├── boot.py              # Boot script (runs on startup)
├── config.py            # Configuration file (WiFi, MQTT, Sensors)
├── main.py              # Main application
├── wifi_manager.py      # WiFi connection management
├── mqtt_client.py       # MQTT client with SSL/TLS support ⭐
├── sensors/             # Sensor drivers
│   ├── ds18b20.py       # DS18B20 temperature sensor
│   ├── ph_sensor.py     # pH sensor (analog)
│   ├── tds_sensor.py    # TDS sensor (analog)
│   └── float_switch.py  # Water level float switch
└── actuators/           # Actuator drivers
    └── relay.py         # Relay controller (pump & light)
```

## 🔒 Security Features

### SSL/TLS MQTT Connection
- **Encrypted Communication**: All sensor data transmitted via TLS/SSL
- **Port**: 8883 (secure MQTT)
- **Certificate Validation**: Server hostname verification
- **Secure Credentials**: Username/password encrypted in transit

### Configuration
```python
# config.py
THINGSPEAK_MQTT_PORT = 8883  # TLS/SSL port
THINGSPEAK_USE_SSL = True    # Enable encryption
```

## 🚀 Quick Start

### 1. Configure Settings

Edit `config.py`:
```python
# WiFi Settings
WIFI_SSID = 'YourWiFiName'
WIFI_PASSWORD = 'YourWiFiPassword'

# ThingSpeak MQTT with SSL/TLS
THINGSPEAK_MQTT_BROKER = 'mqtt3.thingspeak.com'
THINGSPEAK_MQTT_PORT = 8883
THINGSPEAK_USE_SSL = True
THINGSPEAK_CHANNEL_ID = 'YOUR_CHANNEL_ID'
THINGSPEAK_WRITE_API_KEY = 'YOUR_API_KEY'
THINGSPEAK_MQTT_USERNAME = 'YOUR_MQTT_USERNAME'
THINGSPEAK_MQTT_PASSWORD = 'YOUR_MQTT_PASSWORD'
THINGSPEAK_CLIENT_ID = 'YOUR_CLIENT_ID'
```

### 2. Upload to ESP32

Using ampy:
```bash
cd scripts

# Upload main files
ampy --port COM3 put config.py
ampy --port COM3 put wifi_manager.py
ampy --port COM3 put mqtt_client.py
ampy --port COM3 put boot.py
ampy --port COM3 put main.py

# Upload sensor drivers
ampy --port COM3 put sensors sensors

# Upload actuator drivers
ampy --port COM3 put actuators actuators
```

Using rshell:
```bash
rshell --port COM3
> cp *.py /pyboard/
> cp -r sensors /pyboard/
> cp -r actuators /pyboard/
```

### 3. Reset ESP32

Press EN/RST button atau:
```python
>>> import machine
>>> machine.reset()
```

## 📊 Expected Output

```
==================================================
IoT Aquaponik Mini - ESP32
Firmware Version: 1.0.0
==================================================

[Boot] Configuration loaded
[Boot] Free memory: 110000 bytes
[Boot] Boot completed, starting main application...

[System] Initializing...
[MQTT] Client initialized
  Broker: mqtt3.thingspeak.com:8883
  SSL/TLS: Enabled
  Channel: 1234567
[WiFi] Connecting to YourWiFi...
[WiFi] Connected successfully
[MQTT] Connecting to broker...
[MQTT] Using SSL/TLS encryption
[MQTT] Connected successfully
[System] Starting main loop...
[Sensors] Temp: 26.5°C, Water: OK
[Sensors] pH: 6.8
[Sensors] TDS: 450 ppm
[MQTT] Publishing: field1=26.50&field2=6.80&field3=450&field4=1&field5=0&field6=1
[MQTT] Data published successfully
```

## 🔧 Requirements

### Hardware
- ESP32 DevKit V1
- DS18B20 temperature sensor
- pH sensor (analog)
- TDS sensor (analog)
- Float switch
- 2-channel relay module

### Firmware
- **MicroPython**: v1.20 or newer
- **SSL Support**: Required (most recent firmwares include this)
- **Memory**: Minimum 50KB free for SSL/TLS

### Check SSL Support
```python
>>> import ussl
>>> # No error = SSL is supported
```

## 📝 Key Files

### config.py
Configuration file untuk semua settings:
- WiFi credentials
- ThingSpeak MQTT settings (with SSL/TLS)
- Sensor pin mappings
- Threshold values
- Update intervals

### mqtt_client.py ⭐
MQTT client dengan SSL/TLS support:
- Secure connection ke ThingSpeak
- Auto-reconnect functionality
- Data publishing dengan encryption
- Status monitoring

**Key Features:**
```python
class ThingSpeakMQTT:
    def __init__(self, ..., use_ssl=True):
        # SSL/TLS enabled by default
        
    def connect(self):
        # Creates encrypted connection
        if self.use_ssl:
            self.client = MQTTClient(
                ...,
                ssl=True,
                ssl_params={'server_hostname': self.broker}
            )
```

### main.py
Main application loop:
- Sensor reading dengan configurable intervals
- Threshold checking dan alerts
- MQTT data publishing
- WiFi auto-reconnect
- Watchdog timer

### wifi_manager.py
WiFi connection management:
- Auto-connect on boot
- Auto-reconnect on disconnect
- RSSI monitoring
- Connection status

## 🎯 Sensor Reading Intervals

Default intervals (configurable di `config.py`):
- **Temperature**: 30 seconds
- **pH**: 5 minutes (300 seconds)
- **TDS**: 2 minutes (120 seconds)
- **Water Level**: Continuous
- **MQTT Publish**: 60 seconds
- **Status Update**: 1 hour (3600 seconds)

## 🔍 Troubleshooting

### SSL Connection Issues

**Error: "SSL handshake failed"**
```python
# Check SSL support
>>> import ussl

# Check memory
>>> import gc
>>> gc.collect()
>>> gc.mem_free()  # Should be > 50000

# Set system time
>>> import ntptime
>>> ntptime.settime()
```

**Temporary: Disable SSL**
```python
# In config.py
THINGSPEAK_USE_SSL = False
THINGSPEAK_MQTT_PORT = 1883
```

### Memory Issues

```python
# Monitor memory
>>> import gc
>>> gc.collect()
>>> gc.mem_free()

# If low memory, reduce intervals in config.py
SENSOR_READ_INTERVAL = 60  # Increase from 30
PH_READ_INTERVAL = 600     # Increase from 300
```

### WiFi Connection

```python
# Check WiFi status
>>> from wifi_manager import WiFiManager
>>> wifi = WiFiManager('SSID', 'PASSWORD')
>>> wifi.connect()
>>> wifi.get_rssi()
```

## 📚 Documentation

For detailed documentation, see:
- [ESP32_SETUP.md](../docs/ESP32_SETUP.md) - Complete setup guide
- [MQTT_SSL_SECURITY.md](../docs/MQTT_SSL_SECURITY.md) - SSL/TLS security guide
- [THINGSPEAK_SETUP.md](../docs/THINGSPEAK_SETUP.md) - ThingSpeak configuration
- [MIGRATION_SSL_TLS.md](../docs/MIGRATION_SSL_TLS.md) - Migration guide
- [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) - Common issues

## 🔐 Security Best Practices

1. **Always use SSL/TLS** in production
2. **Keep credentials secure** - don't commit to Git
3. **Update firmware regularly** for security patches
4. **Monitor memory usage** for SSL stability
5. **Rotate API keys** periodically

## 📊 Memory Usage

| Component | Memory Usage |
|-----------|--------------|
| Base System | ~30 KB |
| WiFi | ~10 KB |
| MQTT (non-SSL) | ~10 KB |
| MQTT (SSL/TLS) | ~30 KB |
| Sensors | ~5 KB |
| **Total (SSL)** | **~85 KB** |
| **Free (typical)** | **~110 KB** |

## 🆕 Version History

### v1.1 (Current) - SSL/TLS Enabled
- ✅ SSL/TLS MQTT support
- ✅ Port 8883 (secure)
- ✅ Encrypted data transmission
- ✅ Certificate validation
- ✅ Enhanced security

### v1.0 (Previous)
- Basic MQTT support
- Port 1883 (non-secure)
- No encryption

---

**Last Updated**: 2025-12-01  
**Version**: 1.1 (SSL/TLS Enabled)
